# Gemini chatbot

Flask backend + single-page chat UI, streaming replies from the Gemini API.

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export GEMINI_API_KEY=your_key   # from https://aistudio.google.com/apikey
python app.py                    # http://localhost:5000
```

## Deploy on Render
1. Push this folder to a GitHub repo.
2. Render dashboard → New → Blueprint → select the repo (it reads `render.yaml`).
3. Enter `GEMINI_API_KEY` when prompted, then deploy.

Optional env vars: `GEMINI_MODEL` (default `gemini-2.5-flash`), `SYSTEM_PROMPT`.
