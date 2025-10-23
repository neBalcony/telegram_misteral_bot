from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Enum, String
from enum import Enum as PyEnum
 
class Base(DeclarativeBase):
    pass

class UserRole(PyEnum):
    user = "user"
    admin = "admin"

class User(Base):
    __tablename__ = "User" 
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, validate_strings=True), 
                                           default=UserRole.user, 
                                           nullable=False)
    default_request: Mapped[str] = mapped_column(String, nullable=True, default=None)
    
    def __repr__(self):
        return f"uid:{self.id}, role:{self.role}"
    
class Invite(Base):
    __tablename__ = "Invite"
    username: Mapped[str] = mapped_column(String, primary_key=True, nullable=False)
    
    def __repr__(self):
        return f"Invited {self.username}"