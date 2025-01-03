from fastapi import FastAPI

app = FastAPI(title="My FastAPI Project")


@app.get("/health")
def read_root() -> str:
    return "OK"
