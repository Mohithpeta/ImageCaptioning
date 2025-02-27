from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import logging

# Import Stable Diffusion model instance
try:
    from models.image_generation import diffuser
except ImportError as e:
    raise ImportError(f"Failed to import image generation model: {e}")

router = APIRouter()
logger = logging.getLogger(__name__)

# Define request model
class ImageRequest(BaseModel):
    prompt: str

@router.post("/generate")  # Adjusted API route (no "/api" prefix here)
async def generate_image(request: ImageRequest):
    try:
        prompt = request.prompt.strip()
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")

        # Generate image and get saved file path
        image_path = diffuser.generate_image(prompt)

        # Construct the URL using a public-facing path
        image_url = f"/static/generated_images/{os.path.basename(image_path)}"

        logger.info(f"Generated image saved at: {image_path}")

        return {"image_url": image_url}

    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating image: {str(e)}")
