from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from app.models import Student
from app.rabbitmq_consumer import run_consumer
from app.rabbitmq_event import send_message_to_rabbitmq

router = APIRouter()

mongodb_client = MongoClient("user_service_mongodb", 27017)
user_service_db = mongodb_client.user_service

@router.get("/")
def list_all_students():
    try:
        students = user_service_db.students.find()
        return [Student(**student) for student in students]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
def register_new_student(student: Student):
    try:
        student.hash_password()
        student_dict = student.dict()
        result = user_service_db.students.insert_one(student_dict)

        message = f"Student {str(result.inserted_id)} created"
        send_message_to_rabbitmq(f"student.{str(result.inserted_id)}.created", message)

        run_consumer(f"student.{str(result.inserted_id)}.created")

        return {"inserted_id": str(result.inserted_id)}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while registering the student")

@router.get("/{student_id}")
def get_student_information(student_id: str):
    try:
        student_dict = user_service_db.students.find_one(
            {"_id": ObjectId(student_id)},
            {"password": 0}  # Exclude the password field
        )
        if student_dict is None:
            raise HTTPException(status_code=404, detail="Student not found")
        return Student(**student_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{student_id}")
def update_student_information(student_id: str, student: Student):
    try:
        student.hash_password()
        update_data = student.dict(exclude={"id"})
        result = user_service_db.students.update_one({"_id": ObjectId(student_id)}, {"$set": update_data})

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Student not found or no changes made")
        
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
    try:
        # Using soft delete instead of hard delete, so we just update the status field
        result = user_service_db.students.update_one({"_id": ObjectId(student_id)}, {"$set": {"status": "inactive"}})
        
        message = f"Student {str(student_id)} deleted"
        send_message_to_rabbitmq(f"student.{str(student_id)}.deleted", message)

        run_consumer(f"student.{str(student_id)}.deleted")
        
        return {"deleted": result.acknowledged}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))