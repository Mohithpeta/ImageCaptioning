from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import logging

# Import captioner
try:
    from models.image_captioning import captioner
except ImportError:
    raise ImportError("Ensure 'captioner' is correctly defined in 'models.image_captioning'")

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/")
async def generate_caption(image: UploadFile = File(...)):
    """Handles image uploads and generates captions using BLIP."""
    try:
        if not image:
            raise HTTPException(status_code=400, detail="No image uploaded")

        img_data = await image.read()
        if not img_data:
            raise HTTPException(status_code=400, detail="Empty file uploaded")

        try:
            img = Image.open(BytesIO(img_data)).convert("RGB")
        except UnidentifiedImageError:
            raise HTTPException(status_code=400, detail="Uploaded file is not a valid image")

        caption = captioner.generate_description(img_data)
        img.close()

        logger.info(f"Generated caption: {caption}")
        return {"caption": caption}

    except HTTPException as e:
        logger.error(f"HTTP Exception: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
