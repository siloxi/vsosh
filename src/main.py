from fastapi import FastAPI, Response, Cookie, Request
from fastapi.responses import JSONResponse
from typing import Optional
from db import Status, confirm_totp, register, login
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


@app.post("/login")
async def login(response: Response, request: Request):
    body = await request.body()
    body = loads(body.decode())
    response.set_cookie(key="jwt", value="test", httponly=True,samesite="strict") #,secure=True)
    if body["username"] == "go":
        return  "ok"
    return JSONResponse(content="Not found", status_code=400)

@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="jwt")

@app.post("/signup")
async def signup(request: Request):
    body = await request.body()
    body = loads(body.decode())
    return "ok"

@app.get("/confirm-mfa/")
async def confirm_mfa(request: Request, response: Response, code: str):
    jwt = jwtdec(request.cookies['jwt'])
    if jwt is None:
        response.delete_cookie(key="jwt")
        return JSONResponse(content="JWT expired", status_code=400)
    if confirm_totp(jwt['username'], proof=code) == Status.SUCCESS:
        del jwt["required"]
        jwt['valid'] = 1
        response.set_cookie(key="jwt", value=jwtenc(jwt))
        return "ok"
    else:
        return JSONResponse(content="MFA invalid", status_code=400)


# ------
@app.put("/notes/{ID}")
async def put_notes(request: Request, ID: str):
    print(await request.body(), ID)
    return "ok"

@app.patch("/notes/{ID}")
async def update_notes(request: Request, ID: str):
    print(await request.body(), ID)
    return "ok"

@app.delete("/notes/{ID}")
async def delete_notes(request: Request, ID: str):
    print(await request.body(), ID)
    return "ok"

@app.get("/notes")
async def get_notes():
    return {'success': True,
 'data': [{'id': 'note-001',
   'title': 'Project Planning',
   'content': 'Need to finalize the project scope and timeline. Schedule meetings with stakeholders next week.',
   'createdAt': '2026-03-10T14:30:00Z',
   'updatedAt': '2026-03-12T09:15:00Z',
   'userId': 'user-123',
   'tags': ['work', 'planning']},
  {'id': 'note-002',
   'title': 'Shopping List',
   'content': 'Milk, eggs, bread, cheese, tomatoes, lettuce, chicken breast, olive oil',
   'createdAt': '2026-03-11T10:20:00Z',
   'updatedAt': '2026-03-11T10:20:00Z',
   'userId': 'user-123',
   'tags': ['personal', 'shopping']},
  {'id': 'note-003',
   'title': 'JavaScript Tips',
   'content': 'Remember to use const by default, let for loop variables, and avoid var. Always use strict mode. Consider using arrow functions for callbacks.',
   'createdAt': '2026-03-09T16:45:00Z',
   'updatedAt': '2026-03-09T16:45:00Z',
   'userId': 'user-123',
   'tags': ['development', 'javascript']},
  {'id': 'note-004',
   'title': 'Meeting Notes - Q1 Review',
   'content': 'Discussed quarterly goals and progress. Team exceeded targets by 15%. Need to allocate more resources to the new product launch.',
   'createdAt': '2026-03-08T13:00:00Z',
   'updatedAt': '2026-03-08T13:00:00Z',
   'userId': 'user-123',
   'tags': ['work', 'meetings']},
  {'id': 'note-005',
   'title': 'Gym Routine',
   'content': 'Monday: Chest and Triceps, Tuesday: Back and Biceps, Wednesday: Legs, Thursday: Shoulders, Friday: Full Body',
   'createdAt': '2026-03-07T08:30:00Z',
   'updatedAt': '2026-03-07T08:30:00Z',
   'userId': 'user-123',
   'tags': ['fitness', 'personal']},
  {'id': 'note-006',
   'title': 'Book Recommendations',
   'content': 'Atomic Habits by James Clear, The Pragmatic Programmer, Clean Code by Robert Martin, Design Patterns',
   'createdAt': '2026-03-06T11:00:00Z',
   'updatedAt': '2026-03-06T11:00:00Z',
   'userId': 'user-123',
   'tags': ['reading', 'personal']}],
 'count': 6}["data"]



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
