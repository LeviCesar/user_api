from pydantic import BaseModel, EmailStr

# >>>>>>>>>>>> FORMS <<<<<<<<<<<<<<<<<<<

class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str

class FormEmail(BaseModel):
    email: EmailStr


# >>>>>>>>>>>> RESPONSES <<<<<<<<<<<<<<<<<<<