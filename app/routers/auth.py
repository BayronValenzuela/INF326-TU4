from datetime import datetime, timedelta
import bcrypt
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os
import logging
from app.models import Admin, Auth, ChangePassword, Professor, Student
from pydantic import BaseModel

router = APIRouter()

# Conexión a MongoDB
mongodb_client = MongoClient("user_service_mongodb", 27017)
user_service_db = mongodb_client.user_service

# Cargar variables de entorno
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
TOKEN_EXPIRATION_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Datos de prueba para este ejemplo
ALLOWED_ROLES = ["admin", "professor", "student"]

class RoleCheckRequest(BaseModel):
    role: str  # El rol que quieres verificar

# Función para extraer y verificar el token JWT
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        role = payload.get("role")
        if email is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para acceder a este recurso",
            )
        return {"email": email, "role": role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token inválido o expirado",
        )

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
    
# Simulación de autenticación de usuario usando JWT
def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role = payload.get("role")
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No se pudo obtener el rol")
        return {"role": role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")
    
    

@router.post("/authorize")
def authorize(role_check: RoleCheckRequest, current_user: dict = Depends(get_current_user)):
    """
    Endpoint para determinar si un usuario está autorizado de acceder a un recurso.

    Retorna:
    - Comprobación de si el usuario está habilitado o no para acceder al recurso.
    """
    if current_user["role"] == role_check.role:
        return {"message": f"El usuario con rol {current_user['role']} está habilitado para este recurso."}
    
    return {"message": f"El usuario con rol {current_user['role']} NO está habilitado para este recurso."}

@router.post("/recover")
def recover_password(email: str):
    """
    Endpoint para la recuperación de cuentas de estudiantes.

    Parámetro:
    - email: correo del usuario del cual se busca recuperar la contraseña.

    Retorna:
    - token que permite ser utilizado para realizar el cambio de contraseña.
    """
    try:
        # Definir las colecciones a buscar
        collections = [
            {"collection": user_service_db.students, "model": Student},
            {"collection": user_service_db.admins, "model": Admin},
            {"collection": user_service_db.professors, "model": Professor},
        ]
        
        user_data = None

        # Buscar el usuario por email en las colecciones
        for entry in collections:
            user_record = entry["collection"].find_one({"email": email})
            if user_record:
                user_data = entry["model"](**user_record)
                break

        if not user_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

        # Generar un token de recuperación
        expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
        recovery_data = {
            "email": email,
            "exp": expire,
            "action": "recover_password"
        }
        recovery_token = jwt.encode(recovery_data, SECRET_KEY, algorithm=ALGORITHM)

        return {
            "message": "Se ha enviado un enlace para la recuperación de la contraseña.",
            "recovery_token": recovery_token
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al recuperar la contraseña: {str(e)}")

@router.post("/change-password")
def change_password(token: str, new_password: str):
    """
    Endpoint para cambiar la contraseña de un usuario.

    Parámetros:
    - token: token de usuario actual.
    - new_password: nueva contrasña a la cual se desea cambiar.

    Retorna:
    - Un mensaje confirmando que la contraseña fue actualizada o en caso de error, se informa el motivo.
    """
    try:
        # Decodificar y verificar el token de recuperación
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        action = payload.get("action")
        exp = payload.get("exp")

        if email is None or action != "recover_password":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token inválido o acción no permitida")
        
        # Verificar si el token ha expirado
        if datetime.utcnow() > datetime.utcfromtimestamp(exp):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El token ha expirado")

        # Buscar el usuario por email en las colecciones
        collections = [
            {"collection": user_service_db.students, "model": Student},
            {"collection": user_service_db.admins, "model": Admin},
            {"collection": user_service_db.professors, "model": Professor},
        ]
        
        user_data = None
        collection = None

        for entry in collections:
            user_record = entry["collection"].find_one({"email": email})
            if user_record:
                user_data = entry["model"](**user_record)
                collection = entry["collection"]
                break

        if not user_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

        # Hashear la nueva contraseña
        new_hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        # Actualizar la contraseña en la base de datos
        collection.update_one({"email": email}, {"$set": {"password": new_hashed_password}})

        return {"message": "Contraseña actualizada con éxito"}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token inválido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cambiar la contraseña: {str(e)}")
