import torch
from diffusers import AnimateDiffPipeline, DPMSolverMultistepScheduler, MotionAdapter
from diffusers.utils import export_to_gif


class GifGenerator:
    pipe = None

    def __init__(self):
        # Load the motion adapter
        adapter = MotionAdapter.from_pretrained(
            "guoyww/animatediff-motion-adapter-v1-5-2", torch_dtype=torch.float16)
        # load SD 1.5 based finetuned model
        model_id = "emilianJR/epiCRealism"
        pipe = AnimateDiffPipeline.from_pretrained(model_id, motion_adapter=adapter, torch_dtype=torch.float16) 
        scheduler = DPMSolverMultistepScheduler.from_pretrained(
            model_id,
            subfolder="scheduler",
            clip_sample=False,
            solver_order=3,
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
            num_frames=16,
            guidance_scale=7.5,
            num_inference_steps=20,
            generator=torch.Generator("cpu"),
        )
        frames = output.frames[0]
        export_to_gif(frames, path, fps=8)
