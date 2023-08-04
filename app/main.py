from fastapi import FastAPI

from . import models
from .database import engine
from .routers import auth, posts, users, votes

from fastapi.middleware.cors import CORSMiddleware

# Creation of all models tables was replace by the alembic package
# models.Base.metadata.create_all(bind=engine)


# Setup approved origin to send request to our package
origins = ["*"]  #"http://www.google.com"]

# Setup the FstApi and routing
app = FastAPI()
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# general URL i.e.: '127.0.0.1:8000/'
@app.get("/")
async def root():
    return {"message": "Hello World!"}
