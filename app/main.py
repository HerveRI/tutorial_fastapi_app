from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import db_models
from .database import engine
from .routers import post, user, auth, vote

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Used before adding alembic - to create all the tables defined in dbmodels
#db_models.Base.metadata.create_all(bind=engine)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Welcome to my API - Successfuly CI/CD witn DG_Ocean"}