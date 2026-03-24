from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import Base, Note

engine = create_engine("sqlite:///notes.db", echo=True)
session = Session(engine)
Base.metadata.create_all(engine)

def get_notes(uname: str):
    return session.execute(select(Note).where(Note.owner == uname)).fetchall()

def add_note(uname, title, content):
    session.add(Note(title=title, date="2026-03-24T00:00:00Z", content=content, owner=uname, rights=""))
    session.commit()

def edit_note(ID, uname, title, content):
    note = session.query(Note).filter(Note.id == ID).filter(Note.owner == uname).one_or_none()
    note.title = title
    note.content = content
    session.commit()

def delete_note(ID, uname):
    session.query(Note).filter(Note.owner == uname).filter(Note.id == ID).delete()
    session.commit()
