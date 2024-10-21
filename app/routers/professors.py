from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from app.models import Professor

router = APIRouter()

mongodb_client = MongoClient("user_service_mongodb", 27017)
user_service_db = mongodb_client.user_service

@router.get("/")
def list_all_professors():
    try:
        professors = user_service_db.professors.find()
        return [Professor(**professor) for professor in professors]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
def register_new_professor(professor: Professor):
    try:
        professor.hash_password()
        professor_dict = professor.dict()
        result = user_service_db.professors.insert_one(professor_dict)
        return {"inserted_id": str(result.inserted_id)}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while registering the professor")

@router.get("/{professor_id}")
def get_professor_information(professor_id: str):
    try:
        professor_dict = user_service_db.professors.find_one(
            {"_id": ObjectId(professor_id)},
            {"password": 0}  # Exclude the password field
        )
        if professor_dict is None:
            raise HTTPException(status_code=404, detail="Professor not found")
        return Professor(**professor_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{professor_id}")
def update_professor_information(professor_id: str, professor: Professor):
    try:
        professor.hash_password()
        update_data = professor.dict(exclude={"id"})
        result = user_service_db.professors.update_one({"_id": ObjectId(professor_id)}, {"$set": update_data})

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Professor not found or no changes made")

        return {"modified_count": result.modified_count}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while updating the professor")

@router.delete("/{professor_id}")
def delete_professor(professor_id: str):
    try:
        # Using soft delete instead of hard delete, so we just update the status field
        result = user_service_db.professors.update_one({"_id": ObjectId(professor_id)}, {"$set": {"status": "inactive"}})
        return {"deleted": result.acknowledged}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
