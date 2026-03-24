from fastapi import FastAPI, Response, status, HTTPExecution, Depends, APIRouter
from sqlalchemy.orm import Session
from ..import models, schemas, utils
from ..database import get_db


router = APIRouter()

@app.post("/users", status_code =  status.HTTP_201_CREATED, response_model = schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    try:
        print("Incoming user:", user)
    
        hashed_password = utils.hash(user.password)
        print("Hashed password:", hashed_password)
       
        user.password = hashed_password

        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        print("User saved successfully")
    
        return new_user
    except Exception as e:
        print("ERROR", e)
        raise e

@app.get('/users/{id}')
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User,id == id).first()

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail = f"User with id: {id} does not exist")
    
    return user
