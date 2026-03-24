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

class Note(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(40))
    date: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column(String(300))
    rights: Mapped[str] = mapped_column(String(100))
    owner: Mapped[str] = mapped_column(String(32))
