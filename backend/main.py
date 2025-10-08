from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
# from . import database, models, auth, schemas
import database
import models
import auth
import schemas


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Secure 2FA App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return auth.register_user(db, user.username, user.password)

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return auth.login_user(db, user.username, user.password)

@app.post("/enable-2fa/{username}")
def enable_2fa(username: str, db: Session = Depends(get_db)):
    return auth.enable_2fa(db, username)

@app.post("/verify-2fa")
def verify_2fa(data: schemas.TokenVerify, db: Session = Depends(get_db)):
    return auth.verify_2fa(db, data.username, data.code)
