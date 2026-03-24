from fastapi import FastAPI, Response, Cookie, Request
from fastapi.responses import JSONResponse
from typing import Optional
from db import Status, confirm_totp, db_register, db_login
from encoding import jwtenc, jwtdec
from fastapi.middleware.cors import CORSMiddleware
from json import loads
import datetime



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=600
)



# @app.get("/set-cookie/")
# async def set_cookie(response: Response, name: str, value: str):
#     response.set_cookie(key=name, value=value)
        
#     return {
#         "message": f"Cookie '{name}' set"
#     }

# @app.get("/get-cookies/")
# async def get_cookies(request: Request):
#     return {"cookies": dict(request.cookies)}


# @app.get("/delete-cookie/")
# async def delete_cookie(response: Response, name: str):
#     response.delete_cookie(key=name)
#     return {"message": f"Cookie '{name}' removed"}


@app.post("/login")
async def login(response: Response, request: Request):
    body = await request.body()
    body = loads(body.decode())
    #response.set_cookie(key="jwt", value="test", httponly=True,samesite="strict") #,secure=True)
    status = db_login(body["username"], body["password"])
    if status == Status.SUCCESS:
        response.set_cookie(key="jwt", value=jwtenc({"username":body["username"]}), httponly=True,samesite="strict") #,secure=True)
        response.set_cookie(key="username", value=body["username"], httponly=False,samesite="strict") #,secure=True)
        return "Ok"
    if status == Status.TOTP_REQUIRED:
        response.set_cookie(key="jwt", value=jwtenc({"username":'!'+body["username"]}), httponly=True,samesite="strict") #,secure=True)
        return "TOTP required"
    return JSONResponse(content="Invalid username or password", status_code=400)

@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="jwt")
    response.delete_cookie(key="username")

@app.post("/signup")
async def signup(request: Request):
    body = await request.body()
    body = loads(body.decode())
    print(body)
    return "Ok"

@app.post("/confirm-totp/")
async def confirm_mfa(request: Request, response: Response):
    try:
        body = await request.body()
        code = loads(body.decode())["code"]
        jwt = jwtdec(request.cookies['jwt'])
        if jwt is None:
            response.delete_cookie(key="jwt")
            return JSONResponse(content="JWT invalid", status_code=400)
        if jwt['username'][0] != '!':
            return "No action required"
        jwt['username'] = jwt['username'][1:]
        if confirm_totp(jwt['username'], code) == Status.SUCCESS:
            response.set_cookie(key="username", value=jwt["username"], httponly=False,samesite="strict") #,secure=True)
            response.set_cookie(key="jwt", value=jwtenc(jwt))
            return "ok"
        return JSONResponse(content="TOTP invalid", status_code=400)
    except KeyError:
        return JSONResponse(content="Data invalid", status_code=400)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
