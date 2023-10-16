import pytorch_lightning as pl
import sys, gc
import random
import torch
import torchaudio
import typing as tp
import wandb

from aeiou.viz import pca_point_cloud, audio_spectrogram_image, tokens_spectrogram_image
from ema_pytorch import EMA
from einops import rearrange
from torch import optim
from torch.nn import functional as F
from pytorch_lightning.utilities.rank_zero import rank_zero_only

from ..inference.sampling import get_alphas_sigmas, sample
from ..inference.generation import generate_diffusion_cond
from ..models.diffusion import DiffusionModelWrapper, ConditionedDiffusionModelWrapper
from ..models.autoencoders import DiffusionAutoencoder

from time import time

class Profiler:

    def __init__(self):
        self.ticks = [[time(), None]]

    def tick(self, msg):
        self.ticks.append([time(), msg])

    def __repr__(self):
        rep = 80 * "=" + "\n"
        for i in range(1, len(self.ticks)):
            msg = self.ticks[i][1]
            ellapsed = self.ticks[i][0] - self.ticks[i - 1][0]
            rep += msg + f": {ellapsed*1000:.2f}ms\n"
        rep += 80 * "=" + "\n\n\n"
        return rep

class DiffusionUncondTrainingWrapper(pl.LightningModule):
    '''
    Wrapper for training an unconditional audio diffusion model (like Dance Diffusion).
    '''
    def __init__(
            self,
            model: DiffusionModelWrapper,
            lr: float = 1e-4,
    ):
        super().__init__()

        self.diffusion = model
        
        self.diffusion_ema = EMA(
            self.diffusion.model,
            beta=0.9999,
            power=3/4,
            update_every=1,
            update_after_step=1
        )

        self.lr = lr

        self.rng = torch.quasirandom.SobolEngine(1, scramble=True)

    def configure_optimizers(self):
        return optim.Adam([*self.diffusion.parameters()], lr=self.lr)

    def training_step(self, batch, batch_idx):
        reals = batch[0]

        if reals.ndim == 4 and reals.shape[0] == 1:
            reals = reals[0]
        
        # Draw uniformly distributed continuous timesteps
        t = self.rng.draw(reals.shape[0])[:, 0].to(self.device)

        # Calculate the noise schedule parameters for those timesteps
        alphas, sigmas = get_alphas_sigmas(t)

        diffusion_input = reals

        if self.diffusion.pretransform is not None:
            with torch.set_grad_enabled(self.diffusion.pretransform.enable_grad):
                diffusion_input = self.diffusion.pretransform.encode(diffusion_input)

        # Combine the ground truth images and the noise
        alphas = alphas[:, None, None]
        sigmas = sigmas[:, None, None]
        noise = torch.randn_like(diffusion_input)
        noised_inputs = diffusion_input * alphas + noise * sigmas
        targets = noise * alphas - diffusion_input * sigmas

        with torch.cuda.amp.autocast():
            v = self.diffusion(noised_inputs, t)
            mse_loss = F.mse_loss(v, targets)
            loss = mse_loss

        log_dict = {
            'train/loss': loss.detach(),
            'train/mse_loss': mse_loss.detach(),
            'train/std_data': diffusion_input.std(),
        }

        self.log_dict(log_dict, prog_bar=True, on_step=True)
        return loss
    
    def on_before_zero_grad(self, *args, **kwargs):
        self.diffusion_ema.update()

    def export_model(self, path):

        self.diffusion.model = self.diffusion_ema.ema_model

        export_state_dict = {"state_dict": self.diffusion.state_dict()}
        
        torch.save(export_state_dict, path)

class DiffusionUncondDemoCallback(pl.Callback):
    def __init__(self, 
                 demo_every=2000,
                 num_demos=8,
                 demo_steps=250,
                 sample_rate=48000
    ):
        super().__init__()

        self.demo_every = demo_every
        self.num_demos = num_demos
        self.demo_steps = demo_steps
        self.sample_rate = sample_rate
        self.last_demo_step = -1

    @rank_zero_only
    @torch.no_grad()
    def on_train_batch_end(self, trainer, module, outputs, batch, batch_idx):        

        if (trainer.global_step - 1) % self.demo_every != 0 or self.last_demo_step == trainer.global_step:
            return
        
        self.last_demo_step = trainer.global_step

        demo_samples = module.diffusion.sample_size

        if module.diffusion.pretransform is not None:
            demo_samples = demo_samples // module.diffusion.pretransform.downsampling_ratio

        noise = torch.randn([self.num_demos, module.diffusion.io_channels, demo_samples]).to(module.device)

        try:
            fakes = sample(module.diffusion_ema, noise, self.demo_steps, 0)

            if module.diffusion.pretransform is not None:
                fakes = module.diffusion.pretransform.decode(fakes)

            # Put the demos together
            fakes = rearrange(fakes, 'b d n -> d (b n)')

            log_dict = {}
            
            filename = f'demo_{trainer.global_step:08}.wav'
            fakes = fakes.clamp(-1, 1).mul(32767).to(torch.int16).cpu()
            torchaudio.save(filename, fakes, self.sample_rate)

            log_dict[f'demo'] = wandb.Audio(filename,
                                                sample_rate=self.sample_rate,
                                                caption=f'Reconstructed')
        
            log_dict[f'demo_melspec_left'] = wandb.Image(audio_spectrogram_image(fakes))

            trainer.logger.experiment.log(log_dict)

            del fakes
            
        except Exception as e:
            print(f'{type(e).__name__}: {e}')
        finally:
            gc.collect()
            torch.cuda.empty_cache()

class DiffusionCondTrainingWrapper(pl.LightningModule):
    '''
    Wrapper for training a conditional audio diffusion model.
    '''
    def __init__(
            self,
            model: ConditionedDiffusionModelWrapper,
            lr: float = 1e-4,
            causal_dropout: float = 0.0,
    ):
        super().__init__()

        self.diffusion = model
        
        self.diffusion_ema = EMA(
            self.diffusion.model,
            beta=0.9999,
            power=3/4,
            update_every=1,
            update_after_step=1
        )

        self.lr = lr

        self.rng = torch.quasirandom.SobolEngine(1, scramble=True)

        self.causal_dropout = causal_dropout

    def configure_optimizers(self):
        return optim.Adam([*self.diffusion.parameters()], lr=self.lr)

    def training_step(self, batch, batch_idx):
        reals, metadata = batch

        p = Profiler()

        if reals.ndim == 4 and reals.shape[0] == 1:
            reals = reals[0]

        # Draw uniformly distributed continuous timesteps
        t = self.rng.draw(reals.shape[0])[:, 0].to(self.device)

        # Calculate the noise schedule parameters for those timesteps
        alphas, sigmas = get_alphas_sigmas(t)

        diffusion_input = reals

        p.tick("setup")

        with torch.cuda.amp.autocast():
            conditioning = self.diffusion.conditioner(metadata, self.device)
            

        p.tick("conditioning")

        if self.diffusion.pretransform is not None:
            self.diffusion.pretransform.to(self.device)
            with torch.cuda.amp.autocast() and torch.set_grad_enabled(self.diffusion.pretransform.enable_grad):
                diffusion_input = self.diffusion.pretransform.encode(diffusion_input)
                p.tick("pretransform")

        # Combine the ground truth images and the noise
        alphas = alphas[:, None, None]
        sigmas = sigmas[:, None, None]
        noise = torch.randn_like(diffusion_input)
        noised_inputs = diffusion_input * alphas + noise * sigmas
        targets = noise * alphas - diffusion_input * sigmas

        p.tick("noise")

        with torch.cuda.amp.autocast():
            p.tick("amp")
            v = self.diffusion(noised_inputs, t, cond=conditioning, cfg_dropout_prob = 0.1, causal=random.random() < self.causal_dropout)
            p.tick("diffusion")
            mse_loss = F.mse_loss(v, targets)
         
            loss = mse_loss

        log_dict = {
            'train/loss': loss.detach(),
            'train/mse_loss': mse_loss.detach(),
            'train/std_data': diffusion_input.std(),
        }

        self.log_dict(log_dict, prog_bar=True, on_step=True)
        p.tick("log")
        #print(f"Profiler: {p}")
        return loss
    
    def on_before_zero_grad(self, *args, **kwargs):
        self.diffusion_ema.update()

    def export_model(self, path):
        #self.diffusion.model = self.diffusion_ema.ema_model
        export_state_dict = {"state_dict": self.diffusion.state_dict()}
        
        torch.save(export_state_dict, path)

class DiffusionCondDemoCallback(pl.Callback):
    def __init__(self, 
                 demo_every=2000,
                 num_demos=8,
                 sample_size=65536,
                 demo_steps=250,
                 sample_rate=48000,
                 demo_conditioning: tp.Optional[tp.Dict[str, tp.Any]] = {},
                 demo_cfg_scales: tp.Optional[tp.List[int]] = [3, 5, 7],
                 demo_cond_from_batch: bool = False,
                 display_audio_cond: bool = False
    ):
        super().__init__()

        self.demo_every = demo_every
        self.num_demos = num_demos
        self.demo_samples = sample_size
        self.demo_steps = demo_steps
        self.sample_rate = sample_rate
        self.last_demo_step = -1
        self.demo_conditioning = demo_conditioning
        self.demo_cfg_scales = demo_cfg_scales

        # If true, the callback will use the metadata from the batch to generate the demo conditioning
        self.demo_cond_from_batch = demo_cond_from_batch

        # If true, the callback will display the audio conditioning
        self.display_audio_cond = display_audio_cond

    @rank_zero_only
    @torch.no_grad()
    def on_train_batch_end(self, trainer, module: DiffusionCondTrainingWrapper, outputs, batch, batch_idx):        

        if (trainer.global_step - 1) % self.demo_every != 0 or self.last_demo_step == trainer.global_step:
            return

        module.eval()

        print(f"Generating demo")
        self.last_demo_step = trainer.global_step

        demo_samples = self.demo_samples

        demo_cond = self.demo_conditioning

        if self.demo_cond_from_batch:
            # Get metadata from the batch
            demo_cond = batch[1][:self.num_demos]

        if module.diffusion.pretransform is not None:
            demo_samples = demo_samples // module.diffusion.pretransform.downsampling_ratio

        noise = torch.randn([self.num_demos, module.diffusion.io_channels, demo_samples]).to(module.device)

        try:
            print("Getting conditioning")
            with torch.cuda.amp.autocast():
                conditioning = module.diffusion.conditioner(demo_cond, module.device)

            cond_inputs = module.diffusion.get_conditioning_inputs(conditioning)

            log_dict = {}

            if self.display_audio_cond:
                audio_inputs = torch.cat([cond["audio"] for cond in demo_cond], dim=0)
                audio_inputs = rearrange(audio_inputs, 'b d n -> d (b n)')

                filename = f'demo_audio_cond_{trainer.global_step:08}.wav'
                audio_inputs = audio_inputs.clamp(-1, 1).mul(32767).to(torch.int16).cpu()
                torchaudio.save(filename, audio_inputs, self.sample_rate)
                log_dict[f'demo_audio_cond'] = wandb.Audio(filename, sample_rate=self.sample_rate, caption="Audio conditioning")
                log_dict[f"demo_audio_cond_melspec_left"] = wandb.Image(audio_spectrogram_image(audio_inputs))
                trainer.logger.experiment.log(log_dict)

            for cfg_scale in self.demo_cfg_scales:

                print(f"Generating demo for cfg scale {cfg_scale}")
                
                with torch.cuda.amp.autocast():
                    fakes = sample(module.diffusion_ema.model, noise, self.demo_steps, 0, **cond_inputs, cfg_scale=cfg_scale, batch_cfg=True)
                    if module.diffusion.pretransform is not None:
                        fakes = module.diffusion.pretransform.decode(fakes)

                # Put the demos together
                fakes = rearrange(fakes, 'b d n -> d (b n)')

                log_dict = {}
                
                filename = f'demo_cfg_{cfg_scale}_{trainer.global_step:08}.wav'
                fakes = fakes.clamp(-1, 1).mul(32767).to(torch.int16).cpu()
                torchaudio.save(filename, fakes, self.sample_rate)

                log_dict[f'demo_cfg_{cfg_scale}'] = wandb.Audio(filename,
                                                    sample_rate=self.sample_rate,
                                                    caption=f'Reconstructed')
            
                log_dict[f'demo_melspec_left_cfg_{cfg_scale}'] = wandb.Image(audio_spectrogram_image(fakes))

                trainer.logger.experiment.log(log_dict)
            
            del fakes

        except Exception as e:
            raise e
        finally:
            gc.collect()
            torch.cuda.empty_cache()
            module.train()

class DiffusionCondInpaintTrainingWrapper(pl.LightningModule):
    '''
    Wrapper for training a conditional audio diffusion model.
    '''
    def __init__(
            self,
            model: ConditionedDiffusionModelWrapper,
            lr: float = 1e-4,
    ):
        super().__init__()

        self.diffusion = model
        
        self.diffusion_ema = EMA(
            self.diffusion.model,
            beta=0.9999,
            power=3/4,
            update_every=1,
            update_after_step=1
        )

        self.lr = lr

        self.rng = torch.quasirandom.SobolEngine(1, scramble=True)

    def configure_optimizers(self):
        return optim.Adam([*self.diffusion.parameters()], lr=self.lr)

    def random_mask(self, sequence, max_mask_length):

        b, _, sequence_length = sequence.size()

        # Create a mask tensor for each batch element
        masks = []
       # for i in range(b):
        mask_type = random.randint(0, 2)

        if mask_type == 0: # Random mask
            # Randomly choose the length and starting index of the mask
            mask_length = random.randint(1, max_mask_length)
            mask_start = random.randint(0, sequence_length-mask_length)

            # Create the mask tensor
            mask = torch.ones((1, 1, sequence_length))
            mask[:, :, mask_start:mask_start+mask_length] = 0
            mask = mask.to(sequence.device)

            masks.append(mask)
            causal = False

        elif mask_type == 1: # Full mask
            mask = torch.zeros((1, 1, sequence_length)).to(sequence.device)
            masks.append(mask)
            causal = False

        elif mask_type == 2: # Causal mask
            mask = torch.ones((1, 1, sequence_length)).to(sequence.device)
            mask_length = random.randint(1, max_mask_length)
            mask[:, :, -mask_length:] = 0
            masks.append(mask)
            causal = True
                
        # Repeat masks to batch size
        masks = masks * b
        
        # Concatenate the mask tensors into a single tensor
        mask = torch.cat(masks, dim=0).to(sequence.device)

        # Apply the mask to the sequence tensor for each batch element
        masked_sequence = sequence * mask

        return masked_sequence, mask, causal

    def training_step(self, batch, batch_idx):
        reals, metadata = batch

        p = Profiler()

        if reals.ndim == 4 and reals.shape[0] == 1:
            reals = reals[0]

        # Draw uniformly distributed continuous timesteps
        t = self.rng.draw(reals.shape[0])[:, 0].to(self.device)

        # Calculate the noise schedule parameters for those timesteps
        alphas, sigmas = get_alphas_sigmas(t)

        diffusion_input = reals

        p.tick("setup")
        
        with torch.cuda.amp.autocast():
            conditioning = self.diffusion.conditioner(metadata, self.device)

        p.tick("conditioning")

        if self.diffusion.pretransform is not None:
            self.diffusion.pretransform.to(self.device)
            with torch.cuda.amp.autocast() and torch.set_grad_enabled(self.diffusion.pretransform.enable_grad):
                diffusion_input = self.diffusion.pretransform.encode(diffusion_input)
                p.tick("pretransform")

        # Max mask size is the full sequence length
        max_mask_length = diffusion_input.shape[2]

        # Create a mask of random length for a random slice of the input
        masked_input, mask, causal = self.random_mask(diffusion_input, max_mask_length)

        conditioning['inpaint_mask'] = [mask]
        conditioning['inpaint_masked_input'] = [masked_input]

        # Combine the ground truth images and the noise
        alphas = alphas[:, None, None]
        sigmas = sigmas[:, None, None]
        noise = torch.randn_like(diffusion_input)
        noised_inputs = diffusion_input * alphas + noise * sigmas
        targets = noise * alphas - diffusion_input * sigmas

        p.tick("noise")

        with torch.cuda.amp.autocast():
            p.tick("amp")
            v = self.diffusion(noised_inputs, t, cond=conditioning, cfg_dropout_prob = 0.1, causal=causal)
            p.tick("diffusion")
            mse_loss = F.mse_loss(v, targets)
            
            # Check if mse_loss is NaN
            if torch.isnan(mse_loss).any():
                torch.set_printoptions(threshold=10000)
                print("NaN")
                md_string = [f"{md['prompt'], md['seconds_start'], md['seconds_total']}" for md in metadata]
                print(f"Conditioning: {conditioning}")
                print('\n\n'.join(md_string))

            loss = mse_loss

        log_dict = {
            'train/loss': loss.detach(),
            'train/mse_loss': mse_loss.detach(),
            'train/std_data': diffusion_input.std(),
        }

        self.log_dict(log_dict, prog_bar=True, on_step=True)
        p.tick("log")
        #print(f"Profiler: {p}")
        return loss
    
    def on_before_zero_grad(self, *args, **kwargs):
        self.diffusion_ema.update()

    def export_model(self, path):
        self.diffusion.model = self.diffusion_ema.ema_model
        export_state_dict = {"state_dict": self.diffusion.state_dict()}
        
        torch.save(export_state_dict, path)

class DiffusionCondInpaintDemoCallback(pl.Callback):
    def __init__(
        self, 
        demo_dl, 
        demo_every=2000,
        demo_steps=250,
        sample_size=65536,
        sample_rate=48000,
        demo_cfg_scales: tp.Optional[tp.List[int]] = [3, 5, 7]
    ):
        super().__init__()
        self.demo_every = demo_every
        self.demo_steps = demo_steps
        self.demo_samples = sample_size
        self.demo_dl = iter(demo_dl)
        self.sample_rate = sample_rate
        self.demo_cfg_scales = demo_cfg_scales
        self.last_demo_step = -1

    @rank_zero_only
    @torch.no_grad()
    def on_train_batch_end(self, trainer, module: DiffusionCondTrainingWrapper, outputs, batch, batch_idx): 
        if (trainer.global_step - 1) % self.demo_every != 0 or self.last_demo_step == trainer.global_step:
            return
        
        self.last_demo_step = trainer.global_step

        try:
            log_dict = {}

            demo_reals, metadata = next(self.demo_dl)

            # Remove extra dimension added by WebDataset
            if demo_reals.ndim == 4 and demo_reals.shape[0] == 1:
                demo_reals = demo_reals[0]

            demo_reals = demo_reals.to(module.device)


            # Log the real audio
            log_dict[f'demo_reals_melspec_left'] = wandb.Image(audio_spectrogram_image(rearrange(demo_reals, "b d n -> d (b n)").mul(32767).to(torch.int16).cpu()))
            # log_dict[f'demo_reals'] = wandb.Audio(rearrange(demo_reals, "b d n -> d (b n)").mul(32767).to(torch.int16).cpu(), sample_rate=self.sample_rate, caption="demo reals")

            if module.diffusion.pretransform is not None:
                module.diffusion.pretransform.to(module.device)
                with torch.cuda.amp.autocast():
                    demo_reals = module.diffusion.pretransform.encode(demo_reals)

            demo_samples = demo_reals.shape[2]

            # Get conditioning
            conditioning = module.diffusion.conditioner(metadata, module.device)

            masked_input, mask, causal = module.random_mask(demo_reals, demo_reals.shape[2])

            conditioning['inpaint_mask'] = [mask]
            conditioning['inpaint_masked_input'] = [masked_input]

            if module.diffusion.pretransform is not None:
                log_dict[f'demo_masked_input'] = wandb.Image(tokens_spectrogram_image(masked_input.cpu()))
            else:
                log_dict[f'demo_masked_input'] = wandb.Image(audio_spectrogram_image(rearrange(masked_input, "b c t -> c (b t)").mul(32767).to(torch.int16).cpu()))

            cond_inputs = module.diffusion.get_conditioning_inputs(conditioning)

            noise = torch.randn([demo_reals.shape[0], module.diffusion.io_channels, demo_samples]).to(module.device)

            trainer.logger.experiment.log(log_dict)

            for cfg_scale in self.demo_cfg_scales:
                
                print(f"Generating demo for cfg scale {cfg_scale}")
                fakes = sample(module.diffusion_ema.model, noise, self.demo_steps, 0, **cond_inputs, cfg_scale=cfg_scale, batch_cfg=True, causal=causal)

                if module.diffusion.pretransform is not None:
                    with torch.cuda.amp.autocast():
                        fakes = module.diffusion.pretransform.decode(fakes)

                # Put the demos together
                fakes = rearrange(fakes, 'b d n -> d (b n)')

                log_dict = {}
                
                filename = f'demo_cfg_{cfg_scale}_{trainer.global_step:08}.wav'
                fakes = fakes.clamp(-1, 1).mul(32767).to(torch.int16).cpu()
                torchaudio.save(filename, fakes, self.sample_rate)

                log_dict[f'demo_cfg_{cfg_scale}'] = wandb.Audio(filename,
                                                    sample_rate=self.sample_rate,
                                                    caption=f'Reconstructed')
            
                log_dict[f'demo_melspec_left_cfg_{cfg_scale}'] = wandb.Image(audio_spectrogram_image(fakes))

                trainer.logger.experiment.log(log_dict)
        except Exception as e:
            print(f'{type(e).__name__}: {e}')
            raise e

class DiffusionAutoencoderTrainingWrapper(pl.LightningModule):
    '''
    Wrapper for training a diffusion autoencoder
    '''
    def __init__(
            self,
            model: DiffusionAutoencoder,
            lr: float = 1e-4,
            ema_copy = None,
    ):
        super().__init__()

        self.diffae = model
        
        self.diffae_ema = EMA(
            self.diffae,
            ema_model=ema_copy,
            beta=0.9999,
            power=3/4,
            update_every=1,
            update_after_step=1
        )

        self.lr = lr

        self.rng = torch.quasirandom.SobolEngine(1, scramble=True)

    def configure_optimizers(self):
        return optim.Adam([*self.diffae.parameters()], lr=self.lr)

    def training_step(self, batch, batch_idx):
        reals = batch[0]

        if reals.ndim == 4 and reals.shape[0] == 1:
            reals = reals[0]
        
        if self.diffae.pretransform is not None:
            with torch.no_grad():
                reals = self.diffae.pretransform.encode(reals)

        #Encode reals, skipping the pretransform since it was already applied
        latents = self.diffae.encode(reals, skip_pretransform=True)

        latents_upsampled = self.diffae.decode_fn(latents, self.diffae.decoder)

        # Draw uniformly distributed continuous timesteps
        t = self.rng.draw(reals.shape[0])[:, 0].to(self.device)

        # Calculate the noise schedule parameters for those timesteps
        alphas, sigmas = get_alphas_sigmas(t)

        # Combine the ground truth images and the noise
        alphas = alphas[:, None, None]
        sigmas = sigmas[:, None, None]
        noise = torch.randn_like(reals)
        noised_reals = reals * alphas + noise * sigmas
        targets = noise * alphas - reals * sigmas

        with torch.cuda.amp.autocast():
            v = self.diffae.diffusion(noised_reals, t, cond=latents_upsampled)
            mse_loss = F.mse_loss(v, targets)
            loss = mse_loss

        log_dict = {
            'train/loss': loss.detach(),
            'train/mse_loss': mse_loss.detach(),
            'train/std_data': reals.std(),
            'train/latent_std': latents.std(),
        }

        self.log_dict(log_dict, prog_bar=True, on_step=True)
        return loss
    
    def on_before_zero_grad(self, *args, **kwargs):
        self.diffae_ema.update()

    def export_model(self, path):
        export_state_dict = {"state_dict": self.diffae_ema.ema_model.state_dict()}
        
        torch.save(export_state_dict, path)

class DiffusionAutoencoderDemoCallback(pl.Callback):
    def __init__(
        self, 
        demo_dl, 
        demo_every=2000,
        demo_steps=250,
        sample_size=65536,
        sample_rate=48000
    ):
        super().__init__()
        self.demo_every = demo_every
        self.demo_steps = demo_steps
        self.demo_samples = sample_size
        self.demo_dl = iter(demo_dl)
        self.sample_rate = sample_rate
        self.last_demo_step = -1

    @rank_zero_only
    @torch.no_grad()
    def on_train_batch_end(self, trainer, module: DiffusionAutoencoderTrainingWrapper, outputs, batch, batch_idx): 
        if (trainer.global_step - 1) % self.demo_every != 0 or self.last_demo_step == trainer.global_step:
            return
        
        self.last_demo_step = trainer.global_step

        try:
            demo_reals, _ = next(self.demo_dl)

            # Remove extra dimension added by WebDataset
            if demo_reals.ndim == 4 and demo_reals.shape[0] == 1:
                demo_reals = demo_reals[0]

            encoder_input = demo_reals
            
            encoder_input = encoder_input.to(module.device)

            demo_reals = demo_reals.to(module.device)

            with torch.no_grad():
                latents = module.diffae_ema.ema_model.encode(encoder_input)
                fakes = module.diffae_ema.ema_model.decode(latents, steps=self.demo_steps)

            #Interleave reals and fakes
            reals_fakes = rearrange([demo_reals, fakes], 'i b d n -> (b i) d n')

            # Put the demos together
            reals_fakes = rearrange(reals_fakes, 'b d n -> d (b n)')

            log_dict = {}
            
            filename = f'recon_{trainer.global_step:08}.wav'
            reals_fakes = reals_fakes.clamp(-1, 1).mul(32767).to(torch.int16).cpu()
            torchaudio.save(filename, reals_fakes, self.sample_rate)

            log_dict[f'recon'] = wandb.Audio(filename,
                                                sample_rate=self.sample_rate,
                                                caption=f'Reconstructed')

            log_dict[f'embeddings_3dpca'] = pca_point_cloud(latents)
            log_dict[f'embeddings_spec'] = wandb.Image(tokens_spectrogram_image(latents))

            log_dict[f'recon_melspec_left'] = wandb.Image(audio_spectrogram_image(reals_fakes))

            if module.diffae_ema.ema_model.pretransform is not None:
                with torch.no_grad():
                    initial_latents = module.diffae_ema.ema_model.pretransform.encode(encoder_input)
                    first_stage_fakes = module.diffae_ema.ema_model.pretransform.decode(initial_latents)
                    first_stage_fakes = rearrange(first_stage_fakes, 'b d n -> d (b n)')
                    first_stage_fakes = first_stage_fakes.clamp(-1, 1).mul(32767).to(torch.int16).cpu()
                    first_stage_filename = f'first_stage_{trainer.global_step:08}.wav'
                    torchaudio.save(first_stage_filename, first_stage_fakes, self.sample_rate)

                    log_dict[f'first_stage_latents'] = wandb.Image(tokens_spectrogram_image(initial_latents))

                    log_dict[f'first_stage'] = wandb.Audio(first_stage_filename,
                                                sample_rate=self.sample_rate,
                                                caption=f'First Stage Reconstructed')
                    
                    log_dict[f'first_stage_melspec_left'] = wandb.Image(audio_spectrogram_image(first_stage_fakes))
                    

            trainer.logger.experiment.log(log_dict)
        except Exception as e:
            print(f'{type(e).__name__}: {e}')