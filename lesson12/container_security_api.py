from fastapi import FastAPI

app = FastAPI(title="AI Analyst Container Security Lab")


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/info")
def info():
    return {
        "application": "AI Analyst",
        "lesson": "12.7",
        "security": "Hardened container deployment",
    }
