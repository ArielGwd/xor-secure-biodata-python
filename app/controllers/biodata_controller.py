from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.biodata_service import BiodataService
from app.schemas.schema import BiodataCreate 

router = APIRouter(prefix="/api/biodata", tags=["Biodata"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def all_biodata(db: Session = Depends(get_db)):
    return BiodataService.get_all(db)

@router.get("/{id}")
def get_biodata(id: int, db: Session = Depends(get_db)):
    result = BiodataService.get_one(db, id)
    if not result:
        raise HTTPException(404, "Not found")
    return result

@router.post("/")
def create_biodata(payload: BiodataCreate, db: Session = Depends(get_db)):
    obj = BiodataService.create(db, payload)
    return {"id": obj.id, "status": "success"}

@router.put("/{id}")
def update_biodata(id: int, payload: BiodataCreate, db: Session = Depends(get_db)):
    updated = BiodataService.update(db, id, payload)
    if not updated:
        raise HTTPException(404, "Not found")
    return {"status": "updated"}

@router.delete("/{id}")
def delete_biodata(id: int, db: Session = Depends(get_db)):
    ok = BiodataService.delete(db, id)
    if not ok:
        raise HTTPException(404, "Not found")
    return {"status": "deleted"}