from sqlalchemy import Column, String, Boolean, UUID, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    user_id=Column(PG_UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    email=Column(String, unique=True, index=True,nullable=False)
    password_hash=Column(String,nullable=False)
    name=Column(String,nullable=True)
    age=Column(Integer,nullable=True)
    gender=Column(String,nullable=True)
    is_verified=Column(Boolean,default=False)

    token = relationship("UserToken", uselist=False, back_populates="user")

class UserToken(Base):
    __tablename__ = "user_tokens"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True)
    token = Column(String, nullable=False)

    # Relationship to User model
    user = relationship("User", back_populates="token")


