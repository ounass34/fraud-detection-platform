from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import settings

def create_access_token(subject: str, role: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": subject, "role": role, "exp": exp},
                      settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
