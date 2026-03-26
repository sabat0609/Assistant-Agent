from fastapi import FastAPI, Request
from src.agent import agent
import uuid
from datetime import datetime

app = FastAPI()


@app.post("/")
async def handle_message(req: Request):
    body = await req.json()

    try:
        user_text = body["params"]["message"]["parts"][0]["text"]
        session_id = body["params"]["session_id"]

        # run your agent
        result = agent(user_text)

        response_text = result.get("response", result.get("message", ""))

        return {
            "jsonrpc": "2.0",
            "id": body.get("id", str(uuid.uuid4())),
            "result": {
                "artifacts": [
                    {
                        "artifactId": str(uuid.uuid4()),
                        "parts": [
                            {
                                "kind": "text",
                                "text": response_text
                            }
                        ]
                    }
                ],
                "contextId": session_id,
                "kind": "task",
                "status": {
                    "state": "completed",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        }

    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": body.get("id", "error"),
            "error": {
                "code": -32000,
                "message": str(e)
            }
        }
