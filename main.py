from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from domain.crew import crew_router
from domain.sender import sender_router
from domain.shipment import shipment_router

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "http://127.0.0.1",
    "http://localhost",
    "http://localhost:5174",
    "http://api.ssung.app",
    "https://api.ssung.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sender_router.router)
app.include_router(crew_router.router)
app.include_router(shipment_router.router)
