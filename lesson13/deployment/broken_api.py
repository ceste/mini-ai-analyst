from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/health")
def health():
    return JSONResponse(
        status_code=503,
        content={"status": "unhealthy"},
    )


@app.get("/info")
def info():
    return {
        "application": "AI Analyst",
        "version": "broken-test",
    }
