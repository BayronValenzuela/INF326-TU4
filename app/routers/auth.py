from datetime import datetime, timedelta

import bcrypt
from fastapi import APIRouter, HTTPException, status
from jose import jwt
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os
from os.path import join, dirname

import logging
from app.models import Admin, Auth, ChangePassword, Professor, Student

router = APIRouter()

mongodb_client = MongoClient("user_service_mongodb", 27017)
user_service_db = mongodb_client.user_service

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


@router.post("/login")
def authentication(user: Auth):
    try:
        # Buscamos al usuario en las diferentes colecciones
        response_student = user_service_db.students.find_one({"email": user.email})
        response_admin = user_service_db.admins.find_one({"email": user.email})
        response_professor = user_service_db.professors.find_one({"email": user.email})

        data = None
        logging.info("probando si usuario es student")
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
            logging.info("probando si usuario es admin")
            user_admin_dict = Admin(**response_admin)
            if bcrypt.checkpw(
                user.password.encode("utf-8"), user_admin_dict.password.encode("utf-8")
            ):
                data = {
                    "email": user_admin_dict.email,
                    "role": user_admin_dict.role,
                }

        elif response_professor is not None:
            logging.info("probando si usuario es Professor")
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
        logging.info("generando JWT")
        expires_delta = timedelta(minutes=10)
        expire = datetime.utcnow() + expires_delta
        to_encode = data.copy()
        logging.info("update de JWT")
        to_encode.update({"exp": expire})

        logging.info("encoding de JWT")
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logging.info("decoding de JWT")
        decode = jwt.decode(encoded_jwt, SECRET_KEY, algorithms=ALGORITHM)

        return {
            "access_token": encoded_jwt,
            "decoded": decode,
            "token_type": "bearer",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")


@router.post("/authorize")
def authorize():
    try:
        students = user_service_db.students.find()
        return [Student(**student) for student in students]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recover")
def recover():
    try:
        students = user_service_db.students.find()
        return [Student(**student) for student in students]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/change-password")
def change_password(change_data: ChangePassword):
    try:
        user_student = user_service_db.students.find_one({"email": change_data.email})
        user_admin = user_service_db.admins.find_one({"email": change_data.email})
        user_professor = user_service_db.professors.find_one(
            {"email": change_data.email}
        )

        user_data = None
        collection = None

        if user_student:
            user_data = Student(**user_student)
            collection = user_service_db.students
        elif user_admin:
            user_data = Admin(**user_admin)
            collection = user_service_db.admins
        elif user_professor:
            user_data = Professor(**user_professor)
            collection = user_service_db.professors

        if user_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado!"
            )

        # Verificar si la password antigua coincide
        if not bcrypt.checkpw(
            change_data.old_password.encode("utf-8"), user_data.password.encode("utf-8")
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Password antigua no coincide.",
            )

        # Hashear la nueva password
        new_hashed_password = bcrypt.hashpw(
            change_data.new_password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        # Actualizar la password en la base de datos
        collection.update_one(
            {"email": user_data.email}, {"$set": {"password": new_hashed_password}}
        )

        return {"message": "Password updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
