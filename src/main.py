from fastapi import FastAPI, Response, Cookie, Request
from fastapi.responses import JSONResponse
from typing import Optional
from db import check_registration, check_mfa, Status
from encoding import jwtenc, jwtdec
import datetime


'''
нужно организовать базовый вход по паролю и totp
'''
app = FastAPI()

@app.get("/set-cookie/")
async def set_cookie(response: Response, name: str, value: str):
    response.set_cookie(key=name, value=value)
        
    return {
        "message": f"Cookie '{name}' set"
    }

@app.get("/get-cookies/")
async def get_cookies(request: Request):
    return {"cookies": dict(request.cookies)}


@app.get("/delete-cookie/")
async def delete_cookie(response: Response, name: str):
    response.delete_cookie(key=name)
    return {"message": f"Cookie '{name}' removed"}


@app.get("/login/")
async def login(response: Response, request: Request, username: str, password: str):
    #print(Request.base_url.is_secure)
    status = check_registration(username, password)
    if status == Status.SUCCESS:
        response.set_cookie(key="jwt", value=jwtenc({"username": username, "valid": 1}))
        return "ok"
    elif status == Status.SFA_REQUIRED:
        response.set_cookie(key="jwt", value=jwtenc({"username": username, "valid": 0, "required": "2FA"}))
        return "mfa required"
    else:
        return JSONResponse(content="User not found", status_code=400)

@app.get("/confirm-mfa/")
async def confirm_mfa(request: Request, response: Response, code: str):
    jwt = jwtdec(request.cookies['jwt'])
    if jwt is None:
        response.delete_cookie(key="jwt")
        return JSONResponse(content="JWT expired", status_code=400)
    if check_mfa(jwt['username'], proof=code) == Status.SUCCESS:
        del jwt["required"]
        jwt['valid'] = 1
        response.set_cookie(key="jwt", value=jwtenc(jwt))
        return "ok"
    else:
        return JSONResponse(content="MFA invalid", status_code=400)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
