from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db.session import SessionLocal
from app.models.user import User, UserLogins
from app.core.security import hash_password
from app.schemas.user import UserCreate, UserLogin
from app.services.user import UserService
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError

router = APIRouter(prefix="/auth")
security = HTTPBearer()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# JWT functions
def create_jwt(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# ----------------- Register -----------------
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    created_user = service.create_user(user.username, user.email, user.role, user.password)
    return created_user

# ----------------- Login -----------------
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not db_user.verify_password(user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt({"user_id": db_user.id, "role": db_user.role})

    # Save login record
    login_record = UserLogins(
        user_id=db_user.id,
        token=token,
        expiration_date=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    db.add(login_record)
    db.commit()
    db.refresh(login_record)

    return {"access_token": token, "token_type": "bearer"}

# ----------------- Protected route -----------------
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    payload = verify_jwt(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.id == payload.get("user_id")).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {"your authenticated successfully ": current_user}
