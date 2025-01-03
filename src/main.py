from fastapi import FastAPI
import uvicorn

app = FastAPI(title="My FastAPI Project")


@app.get("/health")
def read_root() -> str:
    return "OK"
