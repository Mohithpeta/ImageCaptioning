import { useState, ChangeEvent } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css"; // Make sure to install bootstrap: npm install bootstrap
import "bootstrap-icons/font/bootstrap-icons.css";

const ImageCaption = () => {
  const [image, setImage] = useState<File | null>(null);
  const [caption, setCaption] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [preview, setPreview] = useState<string | null>(null);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      const selectedFile = event.target.files[0];
      setImage(selectedFile);

      // Create preview
      const objectUrl = URL.createObjectURL(selectedFile);
      setPreview(objectUrl);
    }
  };

  const uploadImage = async () => {
    if (!image) {
      alert("Please select an image.");
      return;
    }
    setLoading(true);
    setCaption(null);

    const formData = new FormData();
    formData.append("image", image); // ✅ Backend expects "image", not "file"

    try {
      const response = await axios.post("http://127.0.0.1:8000/caption", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setCaption(response.data.caption);
    } catch (error) {
      console.error("Error uploading image:", error);
      alert("Failed to get caption. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // Custom styles to supplement Bootstrap
  const customStyles = {
    gradientBackground: {
      minHeight: "100vh",
      background: "linear-gradient(135deg, #6a11cb 0%, #2575fc 100%)",
    },
    previewImage: {
      maxHeight: "300px",
      objectFit: "contain" as React.CSSProperties['objectFit'],
    },
    uploadArea: {
      border: "2px dashed #dee2e6",
      borderRadius: "0.375rem",
      cursor: "pointer",
      transition: "all 0.3s ease",
    },
    uploadAreaHover: {
      borderColor: "#6a11cb",
      backgroundColor: "rgba(106, 17, 203, 0.05)",
    },
  };

  return (
    <div style={customStyles.gradientBackground} className="d-flex align-items-center justify-content-center p-3">
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-12 col-md-8 col-lg-6">
            <div className="card shadow-lg">
              <div className="card-header bg-primary text-white text-center py-4">
                <h2 className="mb-0">Image Captioning</h2>
              </div>
              <div className="card-body p-4">
                {preview && (
                  <div className="mb-4 text-center">
                    <img
                      src={preview}
                      alt="Preview"
                      className="img-fluid mb-2 rounded"
                      style={customStyles.previewImage}
                    />
                    <p className="text-muted small">{image?.name}</p>
                  </div>
                )}

                <div
                  className="p-4 text-center mb-4"
                  style={customStyles.uploadArea}
                  onClick={() => document.getElementById("fileInput")?.click()}
                  onMouseOver={(e) => Object.assign(e.currentTarget.style, customStyles.uploadAreaHover)}
                  onMouseOut={(e) => {
                    e.currentTarget.style.borderColor = "#dee2e6";
                    e.currentTarget.style.backgroundColor = "transparent";
                  }}
                >
                  <input
                    id="fileInput"
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    className="d-none"
                  />
                  <div className="mb-3">
                    <i className="bi bi-image" style={{ fontSize: "2rem", color: "#6c757d" }}></i>
                  </div>
                  <p className="text-primary mb-1">{preview ? "Change image" : "Select an image"}</p>
                  <p className="text-muted small">or drag and drop here</p>
                </div>

                <button
                  className="btn btn-primary w-100 py-2"
                  onClick={uploadImage}
                  disabled={loading || !image}
                >
                  {loading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                      Processing...
                    </>
                  ) : (
                    "Generate Caption"
                  )}
                </button>

                {caption && (
                  <div className="alert alert-info mt-4">
                    <h5 className="alert-heading">Generated Caption:</h5>
                    <p className="mb-0">{caption}</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ImageCaption;