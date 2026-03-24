from fastapi import FastAPI, Response,status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas,utils
from app.database import engine, get_db
from sqlalchemy.orm import Session
from app import models



models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# while True:

#     try:
#         conn = psycopg2.connect(host='localhost', database = 'fastapi', user='postgres',password = 'Sql@00', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Databse connection was successfull!")
#         break
#     except Exception as error:
#       print("connecting to database failed")
#       print("Error: ",error)
#       time.sleep(2)

my_posts=[{"title": "title of post 1", "content":"content of post 1", "id": 1}, {"title":
"favorite foods", "content": "I like pizza", "id": 2} ]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p 

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
           return i
   
@app.get("/")
def home():
    return {"message": "Hello FastAPI"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
   posts =  db.query(models.Post).all()
   return {"data": posts}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return{"data": posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
   # cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s)RETURNING 
    #* """,                
     #       (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    #print(**post.model_dump())
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post( **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return{"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int, db:Session = Depends(get_db)):
    #cursor .execute("""SELECT * from posts WHERE id = %s """, (str(id)))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
   # print(post)
    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} was not found")
    return{"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    #if deleted_post == None:
    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} does not exist")
    post.delete(synchronize_session = False)
    db.commit()
    
    return Response(status_code = status.HTTP_204_NO_CONTENT)
 
@app.put("/posts/{id}")
def update_post(id:int, update_post: schemas.PostCreate, db: Session = Depends(get_db)):
   # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""" ,(post.title,post.content,post.published, str(id)))
    
    #updated_post = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.PostCreate).filter(models.PostCreate.id == id)

    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} does not exist")
    post_query.update(update_post.model_dump(), synchoronize_session=False)
    db.commit()
    return post_query.first() 

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

