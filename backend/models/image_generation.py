from diffusers import StableDiffusionPipeline
import torch
import os

# Set environment variable to prevent CUDA memory fragmentation
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

# Load the model with memory optimizations
model_path = "runwayml/stable-diffusion-v1-5"

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
).to("cuda")

# Enable VRAM optimizations
pipe.enable_attention_slicing()
pipe.enable_model_cpu_offload()  # Offload layers to CPU
pipe.enable_xformers_memory_efficient_attention()  # Use xformers for memory-efficient inference

def generate_image(prompt, output_path="output.png", height=384, width=384):
    """
    Generates an image using Stable Diffusion with optimized settings.
    
    :param prompt: Text prompt for image generation
    :param output_path: File path to save the generated image
    :param height: Height of the output image (default: 384 for lower VRAM usage)
    :param width: Width of the output image (default: 384 for lower VRAM usage)
    """
    image = pipe(prompt, height=height, width=width).images[0]
    image.save(output_path)
    return f"Image saved at {output_path}"
