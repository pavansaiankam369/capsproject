from app.models.user import User
from app.core.security import hash_password, is_strong_password
from sqlalchemy.orm import Session
from fastapi import HTTPException

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, username: str, email: str, role: str, password: str):
        from app.repositories.user_repository import UserRepository
        repo = UserRepository(self.db)

        if repo.get_by_email(email):
            raise HTTPException(status_code=400, detail="Email already exists")

        if not is_strong_password(password):
            raise HTTPException(
                status_code=400,
                detail="Password too weak. Must be 8+ chars, include uppercase, lowercase, number & special char."
            )

        new_user = User(
            username=username,
            email=email,
            role=role,
            password=hash_password(password)
        )
        return repo.create(new_user)

    def list_users(self):
        from app.repositories.user_repository import UserRepository
        repo = UserRepository(self.db)
        return repo.list()
