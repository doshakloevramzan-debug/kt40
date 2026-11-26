from fastapi import APIRouter, Depends
from app import auth, models

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/dashboard")
def admin_dashboard(current_user: models.User = Depends(auth.get_current_admin)):
    return {"message": f"Привет, админ {current_user.email}! Это закрытая зона."}