
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


class UpdatePost(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    rating: Optional[int] = None


my_posts = [{"title": "example title", "content": "example content", "id": 1},
            {"title": "example title2", "content": "example content2", "id": 2}
            ]


def find_post(id: int) -> tuple[int, dict]:
    post = [(i, p) for i, p in enumerate(my_posts) if p["id"] == id]
    if not post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Could not find post of id = {id}")

    return post.pop()


class Counter:
    i = len(my_posts)
    def get():
        Counter.i += 1
        return Counter.i


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):

    post_dict = post.dict()
    post_dict['id'] = Counter.get()
    my_posts.append(post_dict)

    return {"data": post_dict}


@app.get("/posts/{id}")
async def get_post(id: int):

    _, post = find_post(id)
    return {"Got post": post}


@app.delete("/posts/{id}")
async def delete_post(id: int):
    idx, _ = find_post(id)
    my_posts.pop(idx)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_post(id: int, post_in: UpdatePost):
    _, curr_post = find_post(id)

    new_post = post_in.dict()
    for k,v in new_post.items():
        if v is not None:
            curr_post[k] = v
    return {"data": curr_post}