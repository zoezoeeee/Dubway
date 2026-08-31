import os

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.bus import router as bus_router
from routes.health import router as health_router
from routes.stations import router as stations_router
from routes.train import router as train_router


app = FastAPI()
app.include_router(health_router)
app.include_router(stations_router)
app.include_router(bus_router)
app.include_router(train_router)

FRONTEND_ORIGINS = os.getenv("FRONTEND_ORIGINS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGINS],
    allow_methods=["GET"],
    allow_headers=["*"],
    allow_credentials=True,
)