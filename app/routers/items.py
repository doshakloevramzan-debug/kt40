from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, auth, database, tasks

router = APIRouter(prefix="/items", tags=["items"])

@router.post("/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    new_item = models.Item(title=item.title, owner_id=current_user.id)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    
    # Вызов фоновой задачи Celery
    tasks.send_notification.delay(current_user.email, new_item.title)
    return new_item

@router.get("/", response_model=list[schemas.Item])
def read_items(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Item).filter(models.Item.owner_id == current_user.id).all()