import os
from flask import Flask, request, Response, jsonify, send_from_directory
from google import genai
from google.genai import types

app = Flask(__name__, static_folder="static")

MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
SYSTEM = os.environ.get("SYSTEM_PROMPT", "You are a helpful, concise assistant.")
_client = None


def client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    return _client


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/healthz")
def health():
    return "ok"


@app.post("/api/chat")
def chat():
    msgs = (request.get_json(silent=True) or {}).get("messages", [])[-30:]
    contents = [
        types.Content(
            role="user" if m.get("role") == "user" else "model",
            parts=[types.Part(text=str(m["content"])[:8000])],
        )
        for m in msgs
        if m.get("content")
    ]
    if not contents or contents[-1].role != "user":
        return jsonify(error="Send at least one user message."), 400

    def stream():
        try:
            for chunk in client().models.generate_content_stream(
                model=MODEL,
                contents=contents,
                config=types.GenerateContentConfig(system_instruction=SYSTEM),
            ):
                if chunk.text:
                    yield chunk.text
        except Exception:
            app.logger.exception("Gemini request failed")
            yield "\n\n[Request failed. Check GEMINI_API_KEY and GEMINI_MODEL in your Render settings.]"

    return Response(
        stream(),
        mimetype="text/plain",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
