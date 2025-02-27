import { useState } from "react";
import axios from "axios";

const ImageGeneration = () => {
  const [prompt, setPrompt] = useState("");
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const apiUrl = "http://127.0.0.1:8000/generate/generate"; // Ensure it matches FastAPI

  const generateImage = async () => {
    if (!prompt.trim()) {
      alert("Enter a valid prompt.");
      return;
    }
    setLoading(true);
    setImageUrl(null);

    try {
      const response = await axios.post(apiUrl, { prompt });

      if (response.data.image_url) {
        setImageUrl(`http://127.0.0.1:8000${response.data.image_url}`);
      } else {
        throw new Error("Invalid response from server.");
      }
    } catch (error) {
      console.error("Error generating image:", error);
      alert("Failed to generate image.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h2>Generate Image from Text</h2>
      <input
        type="text"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter a description..."
      />
      <button onClick={generateImage} disabled={loading || !prompt.trim()}>
        {loading ? "Generating..." : "Generate Image"}
      </button>
      {imageUrl && <img src={imageUrl} alt="Generated" width="300px" />}
    </div>
  );
};

export default ImageGeneration;
