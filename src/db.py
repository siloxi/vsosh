from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import Base, User
from security import password as passlib, totp
from random import choices
from sqlite3 import IntegrityError

engine = create_engine("sqlite:///main.db", echo=True)
session = Session(engine)
Base.metadata.create_all(engine)


# def add_user(**args):
#     session.add(User(**args))
#     session.commit()

class Status:
    # global
    SUCCESS = 0
    ERROR = 1
    # login
    USER_NOT_FOUND = 2
    SECRET_INVALID = 3
    TOTP_REQUIRED = 4
    # registration
    USER_EXIST = 5

def db_login(username: str, password: str) -> int:
    user = session.scalars(select(User).where(User.username == username)).first()
    if user is None:
        return Status.USER_NOT_FOUND
    if passlib.check_hash(user.passhash, password):
        if not bool(user.totp):
            return Status.SUCCESS
        else:
            return Status.TOTP_REQUIRED
    return Status.SECRET_INVALID

def db_register(username: str, password: str) -> int:
    user = session.scalars(select(User).where(User.username == username)).first()
    if user is not None:
        return Status.USER_EXIST
    session.add(User(username=username, passhash=passlib.get_hash(password), aidor=''.join(choices("0123456789abcdefghikmnpqrstuvxyz", k=4))))
    session.commit()
    return Status.SUCCESS

def confirm_totp(username: str, code: str) -> int:
    user = session.scalars(select(User).where(User.username == username)).first()
    if user is None:
        return Status.USER_NOT_FOUND
    if totp.check(int(code), user.totp):
        return Status.SUCCESS
    return Status.SECRET_INVALID
'''
def check_mfa(username: str, proof: str) -> int:
    for i in mdb:
        if i['username'] == username and i['2fa'] == proof:
            return Status.SUCCESS
        else:
            break
    return Status.ERROR
'''
 
if "__main__" == __name__:
    pass
    #check_registration(input(), "happy")
