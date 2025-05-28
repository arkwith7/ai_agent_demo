from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models.models import User
from ..security import get_current_user

router = APIRouter()

@router.get("/me", response_model=User)
def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/settings")
def update_user_settings(settings: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in settings.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user