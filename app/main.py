from fastapi import FastAPI, Response,status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts=[{"title": "title of post 1", "content":"content of post 1", "id":1}, {"title":
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
    return {"messsage":"Hello FastAPI"}

@app.get("/posts")
def get_posts():
    return{"data": my_posts}

@app.post("/createposts")
def create_posts(new_post: Post):
    print(new_post)
    print(new_post.model_dump())
    return{"data": new_post.model_dump()}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} was not found")
    return{"post_detail": post}

@app.delete("/posts/{id}")
def delete_post(id: int):
    # deleting post
    # find the index in the array that has required Id
    # my_posts.pop(index)
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} does not exist")
    my_posts.pop(index)
    return{'message': 'post was succesfully deleted'}
 
@app.put("/posts/{id}")
def update_post(id:int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} does not exist")
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return{"data": post_dict} 