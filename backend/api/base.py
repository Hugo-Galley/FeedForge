import uvicorn
from configuration import setup_logging
from fastapi import FastAPI

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run("api.base:app", host="127.0.0.1", port=8000, reload=True)