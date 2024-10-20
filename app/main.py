from pymongo import MongoClient
from fastapi import FastAPI
from app.routers import professors, students, admins

import logging

app = FastAPI()
mongodb_client = MongoClient("user_service_mongodb", 27017)
user_service_db = mongodb_client.user_service

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

app.include_router(professors.router, prefix="/api/v1/professors", tags=["Professors"])
app.include_router(students.router, prefix="/api/v1/students", tags=["Students"])
app.include_router(admins.router, prefix="/api/v1/admins", tags=["Admins"])
