from logging import raiseExceptions
from app.models import Admin, Professor, Student
from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from bson import ObjectId

from app.models import Student, Admin, Professor, Auth

router = APIRouter()

mongodb_client = MongoClient("user_service_mongodb", 27017)
user_service_db = mongodb_client.user_service

@router.post("/api/v1/auth/login")
## ojito arreglar
def authentication(user: Auth):
    try:
        # buscar input de usuario en la bd
        user_dict = None
        if user.role == "student":
            res = user_service_db.students.find_one({"email": user.email, "password": user.password})
            if res is None:
                raise Exception("user not found, please make sure both email and password are correct")

            user_dict = Student(**res)
        elif user.role == "administrator":
            res = user_service_db.admins.find_one({"email": user.email, "password": user.password})
            if res is None:
                raise Exception("user not found, please make sure both email and password are correct")

            user_dict = Admin(**res)
        elif user.role == "professor":
            res = user_service_db.professors.find_one({"email": user.email, "password": user.password})
            if res is None:
                raise Exception("user not found, please make sure both email and password are correct")

            user_dict = Professor(**res)
        else:
            raise HTTPException(status_code=400, detail=str("Invalid role for user"))

        raise Exception("You are not cooked!")

        # Generar JWT como resultado de una autenticación exitosa para poder utilizar su informacion en la autorizacion posterior


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/v1/auth/authorize")
def list_all_students():
    try:
        students = user_service_db.students.find()
        return [Student(**student) for student in students]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/v1/auth/recover")
def list_all_students():
    try:
        students = user_service_db.students.find()
        return [Student(**student) for student in students]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/v1/auth/change-password")
def list_all_students():
    try:
        students = user_service_db.students.find()
        return [Student(**student) for student in students]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
