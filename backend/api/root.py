from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.rssflow import router as rssflow_router

app = FastAPI()
app.include_router(rssflow_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)