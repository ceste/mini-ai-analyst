from contextlib import asynccontextmanager

from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("STARTUP: Application is initializing")

    yield

    print("SHUTDOWN: Application is stopping")


app = FastAPI(lifespan=lifespan)


@app.get("/hello")
def hello():
    return {"message": "Hello from Mini AI Analyst"}
