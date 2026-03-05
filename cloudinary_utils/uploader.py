import os
import re
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)

IMAGE_FOLDER  = "users/images"
RESUME_FOLDER = "users/resumes"

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
ALLOWED_RESUME_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


def _safe_filename(original_name: str, email: str) -> str:
    """Strip unsafe characters and append email prefix to avoid name collisions."""
    base = original_name.rsplit(".", 1)[0]           
    clean = re.sub(r"[^\w\-]", "_", base)            
    prefix = email.split("@")[0]
    return f"{clean}_{prefix}"


def upload_image(file_bytes: bytes, filename: str, email: str) -> str:
    """
    Upload a profile image to Cloudinary → users/images folder.
    Returns the secure URL.
    """
    result = cloudinary.uploader.upload(
        file_bytes,
        folder=IMAGE_FOLDER,
        public_id=_safe_filename(filename, email),
        resource_type="image",
        overwrite=True,
    )
    return result["secure_url"]


def upload_resume(file_bytes: bytes, filename: str, email: str) -> str:
    """
    Upload a resume (PDF/DOC/DOCX) to Cloudinary → users/resumes folder.
    Uses resource_type='raw' so non-image files are stored correctly.
    Returns the secure URL.
    """
    result = cloudinary.uploader.upload(
        file_bytes,
        folder=RESUME_FOLDER,
        public_id=_safe_filename(filename, email),
        resource_type="raw",
        overwrite=True,
    )
    return result["secure_url"]