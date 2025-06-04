from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.routes import users
from app.db.database import Base, engine
from app.routes import class_router
from app.routes import progress

def create_tables():
    Base.metadata.create_all(bind=engine)
create_tables()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tutor-software.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(class_router.router)

app.include_router(users.router)
app.include_router(progress.router)
@app.get("/")
def welcome_root():
    return {"message": "Welcome to the FastAPI application! It's Running!"}




if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload="True")