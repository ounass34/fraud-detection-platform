from fastapi import APIRouter
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/token")
async def token(username: str, password: str):
    # MVP: remplacer par validation réelle du mot de passe + RBAC.
    return {"access_token": create_access_token(username, "AGENT"), "token_type": "bearer"}
