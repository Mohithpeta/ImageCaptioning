import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from io import BytesIO

class BLIPCaptioner:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to(self.device)
        print("BLIP model loaded successfully!")

    def generate_description(self, image):
        """Generates a caption from a PIL image or file path."""
        if isinstance(image, bytes):
            image = Image.open(BytesIO(image)).convert("RGB")
        elif isinstance(image, str):
            image = Image.open(image).convert("RGB")
        
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)
        output = self.model.generate(
            **inputs,
            max_new_tokens=100,
            num_beams=5,
            do_sample=True,
            min_length=30,
            max_length=100
        )
        return self.processor.decode(output[0], skip_special_tokens=True)

# Initialize model instance
captioner = BLIPCaptioner()
