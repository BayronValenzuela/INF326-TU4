from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from app.models import Admin
from app.rabbitmq_consumer import run_consumer
from app.rabbitmq_event import send_message_to_rabbitmq

router = APIRouter()

mongodb_client = MongoClient("user_service_mongodb", 27017)
user_service_db = mongodb_client.user_service

@router.get("/")
def list_all_admins():
    """
    Endpoint para listar todos los administradores activos.

    **Retorna**:
    - Una lista de todos los administradores con estado 'active'.
    """
    try:
        admins = user_service_db.admins.find({"status":"active"})
        return [Admin(**admin) for admin in admins]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
def register_new_admin(admin: Admin):
    """
    Endpoint para registrar un nuevo administrador.
    
    Parámetros:

    - **ID:** El identificador único asignado automáticamente al administrador.
    - **name:** El nombre del administrador.
    - **role:** El rol asignado al administrador, que define sus privilegios.
    - **email:** La dirección de correo electrónico del administrador, que será única.
    - **password:** La contraseña que se almacenará de forma segura utilizando hash.
    - **status:** El estado del administrador, generalmente 'active' al momento de la creación.

    Retorna:
    - El ID del nuevo administrador registrado.
    """
    try:
        res_email = user_service_db.admins.find_one({"email": admin.email})
        if res_email is None:
            admin.hash_password()
            admin_dict = admin.dict()
            result = user_service_db.admins.insert_one(admin_dict)

            message = f"Administrative {str(result.inserted_id)} created"
            send_message_to_rabbitmq(f"administrative.{str(result.inserted_id)}.created", message)

            run_consumer(f"administrative.{str(result.inserted_id)}.created")

            return {"inserted_id": str(result.inserted_id)}
        else:
            raise Exception("email already registered.")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as ve:
        raise HTTPException(status_code=500, detail=f"An error occurred while registering the admin: {ve}")

@router.get("/{admin_id}")
def get_admin_information(admin_id: str):
    """
    Endpoint para obtener la información de un administrador específico.

    Parámetros:
    - **admin_id:** El ID del administrador.

    Retorna:
    - **id:** El identificador único asignado automáticamente al administrador.
    - **name:** El nombre del administrador.
    - **role:** El rol asignado al administrador, que define sus privilegios.
    - **email:** La dirección de correo electrónico del administrador, que será única.
    - **password:** La contraseña en estado null.
    - **status:** El estado del administrador, generalmente 'active' al momento de la creación.
    """
    admin_dict = {}
    try:
        admin_dict = user_service_db.admins.find_one(
            {"_id": ObjectId(admin_id),"status":"active"},
            {"password": 0},  # Exclude the password field
        )
        if admin_dict is None:
            raise HTTPException(status_code=404, detail="Admin not found")
        return Admin(**admin_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(f"{e}: {admin_dict}"))

@router.put("/{admin_id}")
def update_admin_information(admin_id: str, admin: Admin):
    """
    Endpoint para actualizar la información de un administrador.

    **Parámetros:**
    - **admin_id:** El ID del administrador.
    - **id:** El identificador único asignado automáticamente al administrador.
    - **name:** El nombre del administrador.
    - **role:** El rol asignado al administrador, que define sus privilegios.
    - **email:** La dirección de correo electrónico del administrador, que será única.
    - **password:** La contraseña en estado null.
    - **status:** El estado del administrador, generalmente 'active' al momento de la creación.

    Retorna:
    - El número de registros modificados.
    """
    try:
        admin.hash_password()
        update_data = admin.dict(exclude={"id"})
        result = user_service_db.admins.update_one({"_id": ObjectId(admin_id)}, {"$set": update_data})

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Admin not found or no changes made")

        message = f"Administrative {str(admin_id)} updated"
        send_message_to_rabbitmq(f"administrative.{str(admin_id)}.updated", message)

        run_consumer(f"administrative.{str(admin_id)}.updated")

        return {"modified_count": result.modified_count}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while updating the admin")

@router.delete("/{admin_id}")
def delete_admin(admin_id: str):
    """
    Endpoint para realizar la eliminación lógica (soft delete) de un administrador.

    Parámetros:
    - **admin_id:** El ID del administrador.

    Retorna:
    - Un mensaje confirmando que el administrador ha sido eliminado.
    """
    try:
        # Using soft delete instead of hard delete, so we just update the status field
        result = user_service_db.admins.update_one({"_id": ObjectId(admin_id)}, {"$set": {"status": "inactive"}})

        message = f"Administrative {str(admin_id)} deleted"
        send_message_to_rabbitmq(f"administrative.{str(admin_id)}.deleted", message)

        run_consumer(f"administrative.{str(admin_id)}.deleted")

        return {"deleted": result.acknowledged}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
