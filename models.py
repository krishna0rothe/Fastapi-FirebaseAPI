from pydantic import BaseModel, EmailStr

# Define Pydantic models for data validation
class UserRegistration(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    password: str


class LoginSchema(BaseModel):
    email:EmailStr
    password:str

class UserInDB(BaseModel):
    uid: str
    username: str
    email:EmailStr
    full_name: str
    created_at: str

class Update_user(BaseModel):
    username: str
    email: EmailStr
    full_name: str
