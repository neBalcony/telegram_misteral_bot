from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Enum
from enum import Enum as PyEnum
 
class Base(DeclarativeBase):
    pass

class UserRole(PyEnum):
    user = "user"
    admin = "admin"

class User(Base):
    __tablename__ = "User" 
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, validate_strings=True), 
                                           default=UserRole.user, 
                                           nullable=False)
    
    def __repr__(self):
        return f"uid:{self.id}, role:{self.role}"