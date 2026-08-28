"""
Phase 1 has no auth yet (that's M1 in the roadmap). Every request is
treated as coming from a single seeded student so the registration flow
end-to-end (list meals -> register -> see it reflected) can be built and
demoed honestly, without faking a login screen that doesn't do anything.

When M1 lands, this becomes a real `get_current_student` FastAPI
dependency backed by a JWT, and every route below keeps working
unchanged — it already depends on `get_current_student_id`.
"""
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt

from app.services.auth_service import SECRET_KEY, ALGORITHM

DUMMY_STUDENT_ID = "stu_00001"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def get_current_student_id(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        student_id: str = payload.get("sub")
        if student_id is None:
            raise credentials_exception
        return student_id
    except jwt.PyJWTError:
        raise credentials_exception

CurrentStudentId = Annotated[str, Depends(get_current_student_id)]
