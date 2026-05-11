from fastapi import FastAPI

app = FastAPI(title="EconArena AI")

@app.get("/")
def home():
    return {
        "message": "EconArena AI backend is running"
    }