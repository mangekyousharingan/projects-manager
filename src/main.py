from fastapi import FastAPI
import uvicorn

app = FastAPI(title="My FastAPI Project")


@app.get("/health")
def read_root() -> str:
    return "OK"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # nosec
