from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base, User
engine = create_engine("sqlite:///main.db", echo=True)
session = Session(engine)
Base.metadata.create_all(engine)

def add_user(**args):
    session.add(User(**args))
    session.commit()

mdb = [
    {"username": 'lev', "password": 'lev', "2fa": 'secret'},
    {"username": 'karl', "password": 'mark', "2fa": 'secret'},
    {"username": 'eve', "password": 'hackme', "2fa": False}
]

class Status:
    NO_USER_FOUND = 0
    SUCCESS = 1
    SFA_REQUIRED = 2
    ERROR = 3

def check_registration(username: str, password: str) -> int:
    for i in mdb:
        if i['username'] == username and i['password'] == password:
            if i['2fa']:
                return Status.SFA_REQUIRED
            else:
                return Status.SUCCESS
        else:
            break
    return Status.NO_USER_FOUND

def check_mfa(username: str, proof: str) -> int:
    for i in mdb:
        if i['username'] == username and i['2fa'] == proof:
            return Status.SUCCESS
        else:
            break
    return Status.ERROR
    
