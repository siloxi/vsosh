import jwt
import datetime

SECRET = "secret"
ALGORITHM = "HS256"

def jwtenc(data) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)

def jwtdec(data) -> dict | None:
    try:
        return jwt.decode(data, key=SECRET, algorithms=ALGORITHM)
    except Exception as a:
        print(a)
        return None
        
