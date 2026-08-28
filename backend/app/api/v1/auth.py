import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.repositories.orm_models import StudentORM
from app.schemas.auth import LoginRequest, SignupRequest, Token
from app.services.auth_service import verify_password, get_password_hash, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    # Simple check for existing roll_no (since we use it as unique identifier)
    # The user asked to use id (from table) as primary key login identifier. 
    # But for signup, the id is usually generated. Let's generate one.
    existing = db.query(StudentORM).filter(StudentORM.roll_no == payload.roll_no).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student with this roll number already exists")

    new_id = f"stu_{uuid.uuid4().hex[:10]}"
    student = StudentORM(
        id=new_id,
        name=payload.name,
        roll_no=payload.roll_no,
        hostel=payload.hostel,
        hashed_password=get_password_hash(payload.password)
    )
    db.add(student)
    db.commit()

    # Automatically login after signup
    access_token = create_access_token(data={"sub": student.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    student = db.query(StudentORM).filter(StudentORM.id == payload.id).first()
    if not student:
        raise HTTPException(status_code=401, detail="Incorrect ID or password")
    
    if not verify_password(payload.password, student.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect ID or password")

    access_token = create_access_token(data={"sub": student.id})
    return {"access_token": access_token, "token_type": "bearer"}

from app.core.auth import CurrentStudentId

@router.get("/me")
def get_me(student_id: CurrentStudentId, db: Session = Depends(get_db)):
    student = db.query(StudentORM).filter(StudentORM.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {
        "id": student.id,
        "name": student.name,
        "roll_no": student.roll_no,
        "hostel": student.hostel
    }
