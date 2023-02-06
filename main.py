from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from domain.user import user_router
from domain.crew import crew_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router)
app.include_router(crew_router.router)
