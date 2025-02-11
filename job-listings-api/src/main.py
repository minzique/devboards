from fastapi import FastAPI
from src.api.endpoints import jobs
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import Config

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(jobs.router, prefix="/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Job Listings API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=Config.API_HOST, port=Config.API_PORT)