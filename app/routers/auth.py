from datetime import datetime, timedelta

import bcrypt
from fastapi import APIRouter, HTTPException, status
from jose import jwt
from pymongo import MongoClient

from app.models import Admin, Auth, Professor, Student

router = APIRouter()

mongodb_client = MongoClient("user_service_mongodb", 27017)
user_service_db = mongodb_client.user_service


SECRET_KEY = "Some_Secret_Key"
ALGORITHM = "HS256"


@router.post("/api/v1/auth/login")
## ojito arreglar
def authentication(user: Auth):
    try:
        # Buscamos al usuario en las diferentes colecciones
        response_student = user_service_db.students.find_one({"email": user.email})
        response_admin = user_service_db.admins.find_one({"email": user.email})
        response_professor = user_service_db.professors.find_one({"email": user.email})

        data = None
        if response_student is not None:
            user_student_dict = Student(**response_student)
            if bcrypt.checkpw(
                user.password.encode("utf-8"),
                user_student_dict.password.encode("utf-8"),
            ):
                data = {
                    "email": user_student_dict.email,
                    "role": user_student_dict.role,
                }

        elif response_admin is not None:
            user_admin_dict = Admin(**response_admin)
            if bcrypt.checkpw(
                user.password.encode("utf-8"), user_admin_dict.password.encode("utf-8")
            ):
                data = {
                    "email": user_admin_dict.email,
                    "role": user_admin_dict.role,
                }

        elif response_professor is not None:
            user_professor_dict = Professor(**response_professor)
            if bcrypt.checkpw(
                user.password.encode("utf-8"),
                user_professor_dict.password.encode("utf-8"),
            ):
                data = {
                    "email": user_professor_dict.email,
                    "role": user_professor_dict.role,
                }

        if data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        # Generar el JWT
        expires_delta = timedelta(minutes=30)
        expire = datetime.utcnow() + expires_delta
        to_encode = data.copy()
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return {"access_token": encoded_jwt, "token_type": "bearer"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")


@router.post("/api/v1/auth/authorize")
def authorize():
    try:
        students = user_service_db.students.find()
        return [Student(**student) for student in students]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/v1/auth/recover")
def recover():
    try:
        students = user_service_db.students.find()
        return [Student(**student) for student in students]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/v1/auth/change-password")
def change_password():
    try:
        students = user_service_db.students.find()
        return [Student(**student) for student in students]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
