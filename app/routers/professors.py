from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from app.models import Professor
from app.rabbitmq_consumer import run_consumer
from app.rabbitmq_event import send_message_to_rabbitmq

router = APIRouter()

# Conexión a la base de datos MongoDB
mongodb_client = MongoClient("user_service_mongodb", 27017)
user_service_db = mongodb_client.user_service

@router.get("/")
def list_all_professors():
    """
    Endpoint para listar todos los profesores activos.

    Retorna:
    - Una lista de todos los profesores con estado 'active'.
    """
    try:
        professors = user_service_db.professors.find({"status":"active"})
        return [Professor(**professor) for professor in professors]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
def register_new_professor(professor: Professor):
    """
    Endpoint para registrar un nuevo profesor.

    Parámetros:
    - professor: Un objeto Professor que contiene la información del profesor.
        - **id:** El identificador único asignado automáticamente al profesor.
        - **name:** El nombre del profesor.
        - **role:** El rol asignado al profesor, que define sus privilegios.
        - **email:** La dirección de correo electrónico del profesor, que será única.
        - **password:** La contraseña que se almacenará de forma segura utilizando hash.
        - **status:** El estado del profesor, generalmente 'active' al momento de la creación.
        - **department:** El departamento al que pertenece el profesor.

    Retorna:
    - El ID del nuevo profesor registrado.
    """
    try:
        res_email = user_service_db.professors.find_one({"email": professor.email})
        if res_email is None:
            professor.hash_password()  # Hashear la contraseña del profesor
            professor_dict = professor.dict()
            result = user_service_db.professors.insert_one(professor_dict)

            # Enviar mensaje a RabbitMQ
            message = f"Professor {str(result.inserted_id)} created"
            send_message_to_rabbitmq(f"professor.{str(result.inserted_id)}.created", message)
            run_consumer(f"professor.{str(result.inserted_id)}.created")

            return {"inserted_id": str(result.inserted_id)}
        else:
            raise Exception("email already registered.")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while registering the professor")

@router.get("/{professor_id}")
def get_professor_information(professor_id: str):
    """
    Endpoint para obtener la información de un profesor específico.

    Parámetros:
    - **professor_id:** El ID del profesor.

    Retorna:
    - Los detalles del profesor sin incluir la contraseña.
        - **id:** El identificador único asignado automáticamente al profesor.
        - **name:** El nombre del profesor.
        - **role:** El rol asignado al profesor, que define sus privilegios.
        - **email:** La dirección de correo electrónico del profesor, que será única.
        - **password:** La contraseña en estado null.
        - **status:** El estado del profesor, generalmente 'active' al momento de la creación.
        - **department:** El departamento al que pertenece el profesor.
    """
    try:
        professor_dict = user_service_db.professors.find_one(
            {"_id": ObjectId(professor_id),"status":"active"},
            {"password": 0}  # Excluir el campo de contraseña
        )
        if professor_dict is None:
            raise HTTPException(status_code=404, detail="Professor not found")
        return Professor(**professor_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{professor_id}")
def update_professor_information(professor_id: str, professor: Professor):
    """
    Endpoint para actualizar la información de un profesor.

    Parámetros:
    - professor_id: El ID del profesor.
    - professor: Un objeto Professor con los datos actualizados.
        - **id:** El identificador único asignado automáticamente al profesor.
        - **name:** El nombre del profesor.
        - **role:** El rol asignado al profesor, que define sus privilegios.
        - **email:** La dirección de correo electrónico del profesor, que será única.
        - **password:** La contraseña que se almacenará de forma segura utilizando hash.
        - **status:** El estado del profesor, generalmente 'active' al momento de la creación.
        - **department:** El departamento al que pertenece el profesor.

    Retorna:
    - El número de registros modificados.
    """
    try:
        professor.hash_password()  # Hashear la nueva contraseña
        update_data = professor.dict(exclude={"id"})
        result = user_service_db.professors.update_one({"_id": ObjectId(professor_id)}, {"$set": update_data})

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Professor not found or no changes made")

        # Enviar mensaje a RabbitMQ
        message = f"Professor {str(professor_id)} updated"
        send_message_to_rabbitmq(f"professor.{str(professor_id)}.updated", message)
        run_consumer(f"professor.{str(professor_id)}.updated")

        return {"modified_count": result.modified_count}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while updating the professor")

@router.delete("/{professor_id}")
def delete_professor(professor_id: str):
    """
    Endpoint para realizar la eliminación lógica (soft delete) de un profesor.

    Parámetros:
    - **professor_id:** El ID del profesor.

    Retorna:
    - Un mensaje confirmando que el profesor ha sido eliminado.
    """
    try:
        result = user_service_db.professors.update_one({"_id": ObjectId(professor_id)}, {"$set": {"status": "inactive"}})

        # Enviar mensaje a RabbitMQ
        message = f"Professor {str(professor_id)} deleted"
        send_message_to_rabbitmq(f"professor.{str(professor_id)}.deleted", message)
        run_consumer(f"professor.{str(professor_id)}.deleted")

        return {"deleted": result.acknowledged}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
