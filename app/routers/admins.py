from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from app.models import Admin

router = APIRouter()

mongodb_client = MongoClient("user_service_mongodb", 27017)
user_service_db = mongodb_client.user_service

@router.get("/")
def list_all_admins():
    try:
        admins = user_service_db.admins.find({"status":"active"})
        return [Admin(**admin) for admin in admins]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
def register_new_admin(admin: Admin):
    try:
        res_email = user_service_db.admins.find_one({"email": admin.email})
        if res_email is None:
            admin.hash_password()
            admin_dict = admin.dict()
            result = user_service_db.admins.insert_one(admin_dict)
            return {"inserted_id": str(result.inserted_id)}
        else:
            raise Exception("email already registered.")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as ve:
        raise HTTPException(status_code=500, detail=f"An error occurred while registering the admin: {ve}")

@router.get("/{admin_id}")
def get_admin_information(admin_id: str):
    admin_dict = {}
    try:
        admin_dict = user_service_db.admins.find_one(
            {"_id": ObjectId(admin_id),"status":"active"},
            {"password": 0},  # Exclude the password field
        )
        if admin_dict is None:
            raise Exception("Admin not found")
            raise HTTPException(status_code=404, detail="Admin not found")
        return Admin(**admin_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(f"{e}: {admin_dict}"))

@router.put("/{admin_id}")
def update_admin_information(admin_id: str, admin: Admin):
    try:
        admin.hash_password()
        update_data = admin.dict(exclude={"id"})
        result = user_service_db.admins.update_one({"_id": ObjectId(admin_id)}, {"$set": update_data})

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Admin not found or no changes made")

        return {"modified_count": result.modified_count}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while updating the admin")

@router.delete("/{admin_id}")
def delete_admin(admin_id: str):
    try:
        # Using soft delete instead of hard delete, so we just update the status field
        result = user_service_db.admins.update_one({"_id": ObjectId(admin_id)}, {"$set": {"status": "inactive"}})
        return {"deleted": result.acknowledged}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
