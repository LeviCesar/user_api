from pydantic import BaseModel

# >>>>>>>>>>>> FORMS <<<<<<<<<<<<<<<<<<<

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    
class NewToken(BaseModel):
    access_token: str
    token_type: str


class RefreshToken(BaseModel):
    token: str
    
    
# >>>>>>>>>>>> RESPONSES <<<<<<<<<<<<<<<<<<<