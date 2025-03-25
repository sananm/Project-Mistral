from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bot import GPT

class UserInput(BaseModel):
    userId: int
    prompt: str

app = FastAPI()

viksit = GPT()

items = {
    1 : "First Item",
    2: "Second Item"
}

@app.get("/")
async def read_root():
    return {"message": "Testing"}

@app.get("/test-items/{id}")
async def read_item(id: int, q: str = None):
    print(id, id not in items)
    if id not in items:
        
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": id, "q": items[id]}

@app.post("/ask")
def getResponse(input: UserInput):
    print(input)
    response = viksit.ask(input.prompt)
    return {
        "message": "Received the body",
        "userId": input.userId,
        "prompt": input.prompt,
        "response": response        
    }


@app.post("/exit")
def saveAndClose():
    viksit.exit()
    return {
        "message" : "Saved successfully",
        "status_code" : 200
    }

from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    print(f"HTTP Exception Caught: {exc.detail}")
    return await http_exception_handler(request, exc)

@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    print(f"Unhandled Exception: {repr(exc)}")
    return JSONResponse(status_code=500, content={"message": ":Reaching here"})