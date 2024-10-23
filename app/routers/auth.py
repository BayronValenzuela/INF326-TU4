from datetime import datetime, timedelta
import bcrypt
from fastapi import APIRouter, HTTPException, status
from jose import jwt
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os
import logging
from app.models import Admin, Auth, ChangePassword, Professor, Student

router = APIRouter()

# Conexión a MongoDB
mongodb_client = MongoClient("user_service_mongodb", 27017)
user_service_db = mongodb_client.user_service

# Cargar variables de entorno
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

@router.post("/login")
def authentication(user: Auth):
    """
    Endpoint para autenticar a un usuario basado en email y contraseña.

    Parámetros:
    - **email**: El email del usuario que se desea autenticar.
    - **password**: La contraseña del usuario en texto plano.

    Retorna:
    - **access_token:** El token JWT generado para autenticación.
    - **decoded:** Los datos del token decodificado.
        - **email:** El email del usuario autenticado.
        - **role:** El rol del usuario autenticado.
        - **exp:** La fecha de expiración del token.
    - **token_type:** Tipo de token ('bearer').
    """
    try:
        # Buscar usuario en las colecciones
        response_student = user_service_db.students.find_one({"email": user.email})
        response_admin = user_service_db.admins.find_one({"email": user.email})
        response_professor = user_service_db.professors.find_one({"email": user.email})

        data = None

        if response_student:
            user_student_dict = Student(**response_student)
            if bcrypt.checkpw(user.password.encode("utf-8"), user_student_dict.password.encode("utf-8")):
                data = {"email": user_student_dict.email, "role": user_student_dict.role}
        elif response_admin:
            user_admin_dict = Admin(**response_admin)
            if bcrypt.checkpw(user.password.encode("utf-8"), user_admin_dict.password.encode("utf-8")):
                data = {"email": user_admin_dict.email, "role": user_admin_dict.role}
        elif response_professor:
            user_professor_dict = Professor(**response_professor)
            if bcrypt.checkpw(user.password.encode("utf-8"), user_professor_dict.password.encode("utf-8")):
                data = {"email": user_professor_dict.email, "role": user_professor_dict.role}

        if data is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

        expires_delta = timedelta(minutes=10)
        expire = datetime.utcnow() + expires_delta
        to_encode = data.copy()
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        decode = jwt.decode(encoded_jwt, SECRET_KEY, algorithms=ALGORITHM)

        return {"access_token": encoded_jwt, "decoded": decode, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")

@router.post("/authorize")
def authorize():
    """
    Endpoint para autorizar usuarios y listar estudiantes registrados.

    Retorna:
    - Lista de estudiantes registrados.
    """
    try:
        students = user_service_db.students.find()
        return [Student(**student) for student in students]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recover")
def recover():
    """
    Endpoint para la recuperación de cuentas de estudiantes.

    Retorna:
    - Lista de estudiantes registrados.
    """
    try:
        students = user_service_db.students.find()
        return [Student(**student) for student in students]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/change-password")
def change_password(change_data: ChangePassword):
    """
    Endpoint para cambiar la contraseña de un usuario.

    Parámetros:
    - change_data: Objeto que contiene el email, contraseña antigua y nueva.

    Retorna:
    - Un mensaje confirmando que la contraseña fue actualizada.
    """
    try:
        user_student = user_service_db.students.find_one({"email": change_data.email})
        user_admin = user_service_db.admins.find_one({"email": change_data.email})
        user_professor = user_service_db.professors.find_one({"email": change_data.email})

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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado!")

        if not bcrypt.checkpw(change_data.old_password.encode("utf-8"), user_data.password.encode("utf-8")):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password antigua no coincide.")

        new_hashed_password = bcrypt.hashpw(change_data.new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        collection.update_one({"email": user_data.email}, {"$set": {"password": new_hashed_password}})

        return {"message": "Password updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
