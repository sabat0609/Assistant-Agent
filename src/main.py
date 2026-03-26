from fastapi import FastAPI, Request
from src.agent import agent

app = FastAPI()

@app.post("/")
async def handle(request: Request):
    body = await request.json()

    # SAFE extraction (no session_id dependency)
    params = body.get("params", {})
    message = params.get("message", {})
    parts = message.get("parts", [])

    if not parts:
        return {
            "jsonrpc": "2.0",
            "id": body.get("id", "1"),
            "error": {"code": -32600, "message": "Invalid message format"}
        }

    user_message = parts[0].get("text", "")

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
