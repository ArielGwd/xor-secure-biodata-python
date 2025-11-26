from sqlalchemy.orm import Session
from app.schemas import biodata_schema

class BiodataRepository:

    @staticmethod
    def create(db: Session, obj: biodata_schema.Biodata):
        db.add(obj)
        db.commit()
        db.refresh(obj) # Penting: ambil ID baru dari DB
        return obj

    @staticmethod
    def get_all(db: Session):
        return db.query(biodata_schema.Biodata).order_by(biodata_schema.Biodata.created_at.desc()).all()

    @staticmethod
    def get_by_id(db: Session, id: int):
        return db.query(biodata_schema.Biodata).filter(biodata_schema.Biodata.id == id).first()

    @staticmethod
    def delete(db: Session, obj: biodata_schema.Biodata):
        db.delete(obj)
        db.commit()
        return True