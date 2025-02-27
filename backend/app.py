from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from routes import caption_routes
# from routes import generation_routes

# Initialize FastAPI app
app = FastAPI(title="Image Processing API")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CORS Middleware (Allow all origins for now)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(caption_routes.router, prefix="/caption", tags=["Captioning"])
# app.include_router(generation_routes.router, prefix="/generate", tags=["Image Generation"])

@app.get("/")
async def root():
    logger.info("Root endpoint hit")
    return {"message": "Image Processing API is running"}

# Run the FastAPI server
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI server...")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
