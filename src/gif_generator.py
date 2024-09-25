import torch
from diffusers import AnimateDiffPipeline, DDIMScheduler, MotionAdapter
from diffusers.utils import export_to_gif


class GifGenerator:
    pipe = None

    def __init__(self):
        # Load the motion adapter
        adapter = MotionAdapter.from_pretrained(
            "guoyww/animatediff-motion-adapter-v1-5-2", torch_dtype=torch.float16)
        # load SD 1.5 based finetuned model
        model_id = "SG161222/Realistic_Vision_V5.1_noVAE"
        pipe = AnimateDiffPipeline.from_pretrained(
            model_id, motion_adapter=adapter, torch_dtype=torch.float16)
        scheduler = DDIMScheduler.from_pretrained(
            model_id,
            subfolder="scheduler",
            clip_sample=False,
            timestep_spacing="linspace",
            beta_schedule="linear",
            steps_offset=1,
        )
        pipe.scheduler = scheduler

        # enable memory savings
        pipe.enable_vae_slicing()
        pipe.enable_model_cpu_offload()
        pipe.enable_sequential_cpu_offload()
        pipe.enable_vae_tiling()
        self.pipe = pipe

    def generate_gif(self, prompt, path):
        output = self.pipe(
            height=512,
            width=288,
            prompt=prompt,
            negative_prompt="lowres, text, error, cropped, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, username, watermark, signature",
            num_frames=16,
            guidance_scale=7.5,
            num_inference_steps=25,
            generator=torch.Generator("cpu"),
        )
        frames = output.frames[0]
        export_to_gif(frames, path, fps=8)
