from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    id: str
    password: str

class SignupRequest(BaseModel):
    name: str
    roll_no: str
    hostel: str
    password: str
