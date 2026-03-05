from pydantic import BaseModel
from typing import Optional


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    phone: Optional[str]
    image_url: Optional[str]
    resume_url: Optional[str]
    message: str