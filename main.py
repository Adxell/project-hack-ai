from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from setup.config import settings

#routers
from api.routers import user_router, agent_router, class_router, exam_router

from datetime import datetime

tags_metadata = [
    {
        "name": "User Module",
    },
    {
        "name": "Agent Module",
    },
    {
        "name": "Course Module",
    },
    {
        "name": "Exam Module",
    },
]



app = FastAPI(
    title="Professor AI",
    description="Backend Profesor AI (Python)",
    version="v1.0",
    docs_url=f"/{settings.path_api}/docs",
    redoc_url=f"/{settings.path_api}/redoc",
    openapi_tags=tags_metadata
)


origins = [
    '*',
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router.router, tags=['User Module'], prefix=f'/{settings.path_api}/user')
app.include_router(agent_router.router, tags=['Agent Module'], prefix=f'/{settings.path_api}/agent')
app.include_router(class_router.router, tags=['Course Module'], prefix=f'/{settings.path_api}/course')
app.include_router(exam_router.router, tags=['Exam Module'], prefix=f'/{settings.path_api}/exam')


@app.get("/")
def get():
    return {"mesasge": "ok"}
