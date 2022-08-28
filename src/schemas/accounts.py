from pydantic import BaseModel, EmailStr
from typing import Optional


# >>>>>>>>>>>> FORMS <<<<<<<<<<<<<<<<<<<

class AccountConfigs(BaseModel):
    email: Optional[EmailStr]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    # Others necessary infos...


# >>>>>>>>>>>> RESPONSES <<<<<<<<<<<<<<<<<<<

class Account(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    # Others necessary infos...

class AccountId(BaseModel):
    id: str
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    # Others necessary infos...