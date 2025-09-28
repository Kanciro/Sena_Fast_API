from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.tipo_c_schemas import UserProfileCreate, UserProfileOut, UserAssignmentCreate, UserAssignmentOut
from app.models.tipo_c_models import UserProfile, UserAssignment
from app.auth.auth_handler import decode_access_token
from app.database import get_db

router = APIRouter()

def get_current_user_id(token: str):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    return payload.get("sub")

@router.post("/perfiles", response_model=UserProfileOut, status_code=status.HTTP_201_CREATED)
def create_user_profile(profile: UserProfileCreate, db: Session = Depends(get_db)):
    # Lógica simplificada, asume que el user_id se obtiene del token o de otra manera
    user_id = 1 # HARDCODED para este ejemplo de testing
    db_profile = UserProfile(**profile.dict(), user_id=user_id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.post("/asignaciones", response_model=UserAssignmentOut, status_code=status.HTTP_201_CREATED)
def create_user_assignment(assignment: UserAssignmentCreate, db: Session = Depends(get_db)):
    db_assignment = UserAssignment(**assignment.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.get("/asignaciones/{assignment_id}", response_model=UserAssignmentOut)
def get_user_assignment(assignment_id: int, db: Session = Depends(get_db)):
    db_assignment = db.query(UserAssignment).filter(UserAssignment.id == assignment_id).first()
    if not db_assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asignación no encontrada")
    return db_assignment

@router.put("/perfiles/{profile_id}", response_model=UserProfileOut)
def update_user_profile(profile_id: int, profile: UserProfileCreate, db: Session = Depends(get_db)):
    db_profile = db.query(UserProfile).filter(UserProfile.id == profile_id).first()
    if not db_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil no encontrado")
    
    for key, value in profile.dict().items():
        setattr(db_profile, key, value)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile