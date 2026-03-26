from fastapi import FastAPI, Request
from src.agent import agent

app = FastAPI()

@app.post("/")
async def handle(request: Request):
    body = await request.json()

    user_message = body["params"]["message"]["parts"][0]["text"]

    response = agent(user_message)

    return {
        "jsonrpc": "2.0",
        "id": body.get("id", "1"),
        "result": {
            "artifacts": [
                {
                    "parts": [
                        {
                            "kind": "text",
                            "text": response.get("response", response.get("message", ""))
                        }
                    ]
                }
            ],
            "status": {
                "state": "completed"
            }
        }
    }
