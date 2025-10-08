from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import models
import utils
import database


def register_user(db: Session, username: str, password: str):
    if db.query(models.User).filter(models.User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = utils.hash_password(password)
    user = models.User(username=username, password_hash=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully"}

def login_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not utils.verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if user.is_2fa_enabled:
        return {"2fa_required": True, "username": username}
    return {"message": "Login successful (no 2FA)"}

def enable_2fa(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    secret = utils.generate_otp_secret()
    user.otp_secret = secret
    user.is_2fa_enabled = True
    db.commit()
    return {"qr_code": utils.generate_qr_code_uri(username, secret)}

def verify_2fa(db: Session, username: str, code: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not user.otp_secret:
        raise HTTPException(status_code=400, detail="2FA not enabled")

    if not utils.verify_totp(user.otp_secret, code):
        raise HTTPException(status_code=400, detail="Invalid 2FA code")

    return {"message": "2FA verification successful"}
