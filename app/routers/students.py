from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from app.models import Student
from app.rabbitmq_consumer import run_consumer
from app.rabbitmq_event import send_message_to_rabbitmq

router = APIRouter()

# Conexión a la base de datos MongoDB
mongodb_client = MongoClient("user_service_mongodb", 27017)
user_service_db = mongodb_client.user_service

@router.get("/")
def list_all_students():
    """
    Endpoint para listar todos los estudiantes activos.

    Retorna:
    - Una lista de todos los estudiantes con estado 'active'.

    """
    try:
        students = user_service_db.students.find({"status":"active"})
        return [Student(**student) for student in students]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
def register_new_student(student: Student):
    """
    Endpoint para registrar un nuevo estudiante.

    Parámetros:

    - **id:** El identificador único asignado automáticamente al estudiante.
    - **name:** El nombre del estudiante.
    - **role:** El rol asignado al estudiante, que define sus privilegios.
    - **email:** La dirección de correo electrónico del estudiante, que será única.
    - **password:** La contraseña que se almacenará de forma segura utilizando hash.
    - **status:** El estado del estudiante, generalmente 'active' al momento de la creación.
    - **major:** La carrera a la que pertenece el estudiante.

    Retorna:
    - El ID del nuevo estudiante registrado.

    """
    try:
        res_email = user_service_db.students.find_one({"email": student.email})
        if res_email is None:
            student.hash_password()  # Hashear la contraseña del estudiante
            student_dict = student.dict()
            result = user_service_db.students.insert_one(student_dict)

            # Enviar mensaje a RabbitMQ
            message = f"Student {str(result.inserted_id)} created"
            send_message_to_rabbitmq(f"student.{str(result.inserted_id)}.created", message)
            run_consumer(f"student.{str(result.inserted_id)}.created")

            return {"inserted_id": str(result.inserted_id)}
        else:
            raise Exception("email already registered.")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        HTTPException(status_code=500, detail=f"An error occurred while registering the student: {str(e)}")

@router.get("/{student_id}")
def get_student_information(student_id: str):
    """
    Endpoint para obtener la información de un estudiante específico.

    Parámetros:
    - **student_id**: El ID del estudiante.

    Retorna:
    - Los detalles del estudiante sin incluir la contraseña.
        - **id:** El identificador único asignado automáticamente al estudiante.
        - **name:** El nombre del estudiante.
        - **role:** El rol asignado al estudiante, que define sus privilegios.
        - **email:** La dirección de correo electrónico del estudiante, que será única.
        - **password:** La contraseña en estado null.
        - **status:** El estado del estudiante, generalmente 'active' al momento de la creación.
        - **major:** La carrera a la que pertenece el estudiante.

    """
    try:
        student_dict = user_service_db.students.find_one(
            {"_id": ObjectId(student_id),"status":"active"},
            {"password": 0}  # Excluir el campo de contraseña
        )
        if student_dict is None:
            raise HTTPException(status_code=404, detail="Student not found")
        return Student(**student_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{student_id}")
def update_student_information(student_id: str, student: Student):
    """
    Endpoint para actualizar la información de un estudiante.

    Parámetros:
    - **student_id**: El ID del estudiante.
    - **student**: Un objeto Student con los datos actualizados.
        - **id:** El identificador único asignado automáticamente al estudiante.
        - **name:** El nombre del estudiante.
        - **role:** El rol asignado al estudiante, que define sus privilegios.
        - **email:** La dirección de correo electrónico del estudiante, que será única.
        - **password:** La contraseña en estado null.
        - **status:** El estado del estudiante, generalmente 'active' al momento de la creación.
        - **major:** La carrera a la que pertenece el estudiante.

    Retorna:
    - El número de registros modificados.

    """
    try:
        student.hash_password()  # Hashear la nueva contraseña
        update_data = student.dict(exclude={"id"})
        result = user_service_db.students.update_one({"_id": ObjectId(student_id)}, {"$set": update_data})

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Student not found or no changes made")

        # Enviar mensaje a RabbitMQ
        message = f"Student {str(student_id)} updated"
        send_message_to_rabbitmq(f"student.{str(student_id)}.updated", message)
        run_consumer(f"student.{str(student_id)}.updated")

        return {"modified_count": result.modified_count}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while updating the student")

@router.delete("/{student_id}")
def delete_student(student_id: str):
    """
    Endpoint para realizar la eliminación lógica (soft delete) de un estudiante.

    Parámetros:
    - **student_id**: El ID del estudiante.

    Retorna:
    - Un mensaje confirmando que el estudiante ha sido eliminado.
    """
    try:
        result = user_service_db.students.update_one({"_id": ObjectId(student_id)}, {"$set": {"status": "inactive"}})

        # Enviar mensaje a RabbitMQ
        message = f"Student {str(student_id)} deleted"
        send_message_to_rabbitmq(f"student.{str(student_id)}.deleted", message)
        run_consumer(f"student.{str(student_id)}.deleted")

        return {"deleted": result.acknowledged}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
