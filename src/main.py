from fastapi import FastAPI
from pydantic import BaseModel
from src.agent import agent

app = FastAPI()

class Request(BaseModel):
    query: str

@app.get("/")
def home():
    return {"message": "AI Support Agent Running 🚀"}

@app.post("/chat")
def chat(req: Request):
    return agent(req.query)