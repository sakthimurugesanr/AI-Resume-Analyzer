import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import re
import asyncpg
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from db.database import get_connection
from db.schema import create_tables
from models.user import UserResponse
from cloudinary_utils.uploader import (
    upload_image,
    upload_resume,
    ALLOWED_IMAGE_TYPES,
    ALLOWED_RESUME_TYPES,
)

app = FastAPI(title="User Registration API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await create_tables()


# ─── Helper ──────────────────────────────────────────────────────────────────
def validate_phone(phone: str) -> bool:
    return bool(re.match(r"^\+?[\d\s\-()]{7,20}$", phone))


@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(
    username: str                  = Form(..., description="Full name"),
    email:    str                  = Form(..., description="Email address"),
    role:     str                  = Form(..., description="Role e.g. developer, designer"),
    phone:    Optional[str]        = Form(None, description="Phone number"),
    image:    Optional[UploadFile] = File(None, description="Profile image (JPEG/PNG/WEBP)"),
    resume:   Optional[UploadFile] = File(None, description="Resume (PDF/DOC/DOCX)"),
):
    if phone and not validate_phone(phone):
        raise HTTPException(status_code=422, detail="Invalid phone number format.")

    image_url: Optional[str] = None
    if image:
        if image.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid image type '{image.content_type}'. Allowed: JPEG, PNG, WEBP, GIF.",
            )
        try:
            image_url = upload_image(await image.read(), image.filename, email)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Image upload failed: {e}")

    resume_url: Optional[str] = None
    if resume:
        if resume.content_type not in ALLOWED_RESUME_TYPES:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid resume type '{resume.content_type}'. Allowed: PDF, DOC, DOCX.",
            )
        try:
            resume_url = upload_resume(await resume.read(), resume.filename, email)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Resume upload failed: {e}")

    conn = await get_connection()
    try:
        row = await conn.fetchrow(
            """
            INSERT INTO users (username, email, role, phone, image_url, resume_url)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id, username, email, role, phone, image_url, resume_url
            """,
            username, email, role, phone, image_url, resume_url,
        )
    except asyncpg.UniqueViolationError:
        raise HTTPException(status_code=409, detail="A user with this email already exists.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        await conn.close()

    return UserResponse(**dict(row), message="User registered successfully.")


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    conn = await get_connection()
    try:
        row = await conn.fetchrow(
            "SELECT id, username, email, role, phone, image_url, resume_url FROM users WHERE id = $1",
            user_id,
        )
    finally:
        await conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="User not found.")

    return UserResponse(**dict(row), message="User fetched successfully.")


@app.get("/health")
async def health():
    return {"status": "ok"}