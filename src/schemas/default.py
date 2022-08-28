from pydantic import BaseModel
from typing import Union

# >>>>>>>>>>>> DEFAULT RESPONSES <<<<<<<<<<<<<<<<<<<

class Default(BaseModel):
    message: str