from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(36), unique=True)
    aidor: Mapped[str] = mapped_column(String(4)) # anti idor
    passhash: Mapped[Optional[str]] = None
    totp: Mapped[Optional[int]] = None
    # addresses: Mapped[List["Address"]] = relationship(
    #      cascade="all, delete-orphan"
    # )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"

class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
