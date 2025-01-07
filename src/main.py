from fastapi import FastAPI

from src.adapters.fastapi.api import api_router
from src.adapters.fastapi.utils import lifespan, unhandled_exception_handler

app = FastAPI(title="Projects manager API", lifespan=lifespan)

app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(router=api_router)
