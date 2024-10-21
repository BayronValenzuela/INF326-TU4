import logging

from fastapi import FastAPI
from pymongo import MongoClient

from app.routers import admins, auth, professors, students

app = FastAPI()
mongodb_client = MongoClient("user_service_mongodb", 27017)
user_service_db = mongodb_client.user_service

"""
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(name)s:%(message)s"
)
"""

app.include_router(professors.router, prefix="/api/v1/professors", tags=["Professors"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authenticate"])
app.include_router(students.router, prefix="/api/v1/students", tags=["Students"])
app.include_router(admins.router, prefix="/api/v1/admins", tags=["Admins"])
