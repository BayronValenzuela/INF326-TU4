from pydantic import BaseModel
from bson import ObjectId
from typing import Optional
from pydantic import Field

import bcrypt

class User(BaseModel):
    id: str | None = None
    name: str
    email: str
    password: str | None = None
    status: Optional[str] = Field(default="active")

    def __init__(self, **kargs):
        if "_id" in kargs:
            kargs["id"] = str(kargs["_id"])
        super().__init__(**kargs)

    def hash_password(self):
        self.password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
    }


class Professor(User):
    department: str

class Student(User):
    major: str

class Admin(User):
    pass