from pymongo import MongoClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import professors, students, admins

import logging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],  # Permitir todas las orígenes, puedes restringir esto según sea necesario
    allow_credentials=True,
    allow_methods=[""],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

mongodb_client = MongoClient("user_service_mongodb", 27017)
user_service_db = mongodb_client.user_service

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

app.include_router(professors.router, prefix="/api/v1/professors", tags=["Professors"])
app.include_router(students.router, prefix="/api/v1/students", tags=["Students"])
app.include_router(admins.router, prefix="/api/v1/admins", tags=["Admins"])
