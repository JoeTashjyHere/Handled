import uuid

from fastapi import Depends, HTTPException, Request, Response
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from sqlalchemy.orm import Session

from .config import settings
from .db import get_db
from .models import User

serializer = URLSafeTimedSerializer(settings.MAGIC_LINK_SECRET, salt="handled-magic")


def make_magic_token(email: str) -> str:
    return serializer.dumps({"email": email})


def verify_magic_token(token: str, max_age_seconds: int = 15 * 60) -> str:
    try:
        data = serializer.loads(token, max_age=max_age_seconds)
        return data["email"]
    except SignatureExpired:
        raise HTTPException(status_code=400, detail="Magic link expired. Request a new one.")
    except BadSignature:
        raise HTTPException(status_code=400, detail="Invalid magic link token.")


def set_session_cookie(resp: Response, user_id: str):
    session_token = serializer.dumps({"user_id": user_id}, salt="handled-session")
    resp.set_cookie(
        key=settings.SESSION_COOKIE_NAME,
        value=session_token,
        httponly=True,
        secure=False if settings.ENV == "dev" else True,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,
    )


def clear_session_cookie(resp: Response):
    resp.delete_cookie(settings.SESSION_COOKIE_NAME)


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    raw = request.cookies.get(settings.SESSION_COOKIE_NAME)
    if not raw:
        raise HTTPException(status_code=401, detail="Not authenticated.")
    try:
        data = serializer.loads(raw, max_age=60 * 60 * 24 * 30, salt="handled-session")
        user_id = data["user_id"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid session.")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")
    return user


def get_or_create_user(db: Session, email: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if user:
        return user
    user = User(id=str(uuid.uuid4()), email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
