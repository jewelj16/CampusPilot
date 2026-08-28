from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    roll_no: str
    password: str

class SignupRequest(BaseModel):
    name: str
    roll_no: str
    hostel: str
    password: str
