import jwt
import datetime

SECRET = "sefi3m2om2o3i23f0i2mf3efef323"
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
        
