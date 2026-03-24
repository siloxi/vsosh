# FASTAPI LOGIC
from fastapi import FastAPI, Response, Cookie, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from db import get_notes, add_note, delete_note, edit_note
from encoding import jwtdec
from json import loads

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=600,  
)


# @app.put("/notes/{ID}")
# async def put_notes(request: Request, ID: str):
#     body = await request.body()
#     return "ok"


@app.post("/notes")
async def post_notes(request: Request):
    body = await request.body()
    body = loads(body.decode())
    jwt = jwtdec(request.cookies['jwt'])
    if jwt is None:
        response = JSONResponse(content="JWT invalid", status_code=400)
        response.delete_cookie(key="jwt")
        response.delete_cookie(key="username")
        return response
    add_note(jwt["username"], body["title"], body["content"])
    return "ok"

@app.put("/notes/{ID}")
async def update_notes(request: Request, ID: str):
    body = await request.body()
    body = loads(body.decode())
    jwt = jwtdec(request.cookies['jwt'])
    if jwt is None:
        response = JSONResponse(content="JWT invalid", status_code=400)
        response.delete_cookie(key="jwt")
        response.delete_cookie(key="username")
        return response
    edit_note(ID, jwt["username"], body["title"], body["content"])
    return "ok"

@app.delete("/notes/{ID}")
async def delete_notes(request: Request, ID: str):
    jwt = jwtdec(request.cookies['jwt'])
    if jwt is None:
        response = JSONResponse(content="JWT invalid", status_code=400)
        response.delete_cookie(key="jwt")
        response.delete_cookie(key="username")
        return response
    delete_note(ID, jwt["username"])
    #print(await request.body(), ID)
    return "ok"
# session.add(Note(title="Заметка 1", date="2026-03-10T14:30:12Z", content="Первая заметка Ивана", owner="ivan", rights=""))
@app.get("/notes")
async def get_note(request: Request):
    jwt = jwtdec(request.cookies['jwt'])
    if jwt is None:
        response = JSONResponse(content="JWT invalid", status_code=400)
        response.delete_cookie(key="jwt")
        response.delete_cookie(key="username")
        return response
    res = []
    for i in get_notes(jwt["username"]):
        i = i[0]
        res.append({"id":i.id, "title": i.title, "content": i.content, "createdAt": i.date, "updatedAt": i.date, "userId": i.owner, "tags":[]})
    return res
 #    return {'success': True,
 # 'data': [{'id': 'note-001',
 #   'title': 'Project Planning',
 #   'content': 'Need to finalize the project scope and timeline. Schedule meetings with stakeholders next week.',
 #   'createdAt': '2026-03-10T14:30:00Z',
 #   'updatedAt': '2026-03-12T09:15:00Z',
 #   'userId': 'user-123',
 #   'tags': ['work', 'planning']},
 #  {'id': 'note-002',
 #   'title': 'Shopping List',
 #   'content': 'Milk, eggs, bread, cheese, tomatoes, lettuce, chicken breast, olive oil',
 #   'createdAt': '2026-03-11T10:20:00Z',
 #   'updatedAt': '2026-03-11T10:20:00Z',
 #   'userId': 'user-123',
 #   'tags': ['personal', 'shopping']},
 #  {'id': 'note-003',
 #   'title': 'JavaScript Tips',
 #   'content': 'Remember to use const by default, let for loop variables, and avoid var. Always use strict mode. Consider using arrow functions for callbacks.',
 #   'createdAt': '2026-03-09T16:45:00Z',
 #   'updatedAt': '2026-03-09T16:45:00Z',
 #   'userId': 'user-123',
 #   'tags': ['development', 'javascript']},
 #  {'id': 'note-004',
 #   'title': 'Meeting Notes - Q1 Review',
 #   'content': 'Discussed quarterly goals and progress. Team exceeded targets by 15%. Need to allocate more resources to the new product launch.',
 #   'createdAt': '2026-03-08T13:00:00Z',
 #   'updatedAt': '2026-03-08T13:00:00Z',
 #   'userId': 'user-123',
 #   'tags': ['work', 'meetings']},
 #  {'id': 'note-005',
 #   'title': 'Gym Routine',
 #   'content': 'Monday: Chest and Triceps, Tuesday: Back and Biceps, Wednesday: Legs, Thursday: Shoulders, Friday: Full Body',
 #   'createdAt': '2026-03-07T08:30:00Z',
 #   'updatedAt': '2026-03-07T08:30:00Z',
 #   'userId': 'user-123',
 #   'tags': ['fitness', 'personal']},
 #  {'id': 'note-006',
 #   'title': 'Book Recommendations',
 #   'content': 'Atomic Habits by James Clear, The Pragmatic Programmer, Clean Code by Robert Martin, Design Patterns',
 #   'createdAt': '2026-03-06T11:00:00Z',
 #   'updatedAt': '2026-03-06T11:00:00Z',
 #   'userId': 'user-123',
 #   'tags': ['reading', 'personal']}],
 # 'count': 6}["data"]



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
