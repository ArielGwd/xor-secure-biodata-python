from sqlalchemy.orm import Session
from app.core.xor_encryption import xor_encrypt, xor_decrypt
from app.core.config import SECRET_KEY
from app.schemas import biodata_schema
from app.repositories.biodata_repository import BiodataRepository
from app.schemas.schema import BiodataCreate

class BiodataService:

    @staticmethod
    def get_all(db: Session):
        rows = BiodataRepository.get_all(db)
        results = []

        for r in rows:
            decrypted_email = ""
            decrypted_phone = ""
            decrypted_address = ""

            try:
                decrypted_email = xor_decrypt(r.email, SECRET_KEY)
                decrypted_phone = xor_decrypt(r.phone, SECRET_KEY)
                decrypted_address = xor_decrypt(r.address, SECRET_KEY) if r.address else ""
            except Exception:
                decrypted_email = r.email
                decrypted_phone = r.phone
                decrypted_address = r.address

            results.append({
                "id": r.id,
                "name": r.name,
                "email": decrypted_email,
                "phone": decrypted_phone,
                "address": decrypted_address,
                "gender": r.gender,
                "created_at": r.created_at.isoformat()
            })

        return results

    @staticmethod
    def get_one(db: Session, id: int):
        r = BiodataRepository.get_by_id(db, id)
        if not r:
            return None

        return {
            "id": r.id,
            "name": r.name,
            "email": xor_decrypt(r.email, SECRET_KEY),
            "phone": xor_decrypt(r.phone, SECRET_KEY),
            "address": xor_decrypt(r.address, SECRET_KEY) if r.address else "",
            "gender": r.gender,
            "created_at": r.created_at.isoformat(),
        }

    @staticmethod
    def create(db: Session, data: BiodataCreate):
        obj = biodata_schema.Biodata(
            name=data.name,
            email=xor_encrypt(data.email, SECRET_KEY),
            phone=xor_encrypt(data.phone, SECRET_KEY),
            address=xor_encrypt(data.address, SECRET_KEY),
            gender=data.gender
        )
        return BiodataRepository.create(db, obj)

    @staticmethod
    def update(db: Session, id: int, data: BiodataCreate):
        r = BiodataRepository.get_by_id(db, id)
        if not r:
            return None

        r.name = data.name
        r.email = xor_encrypt(data.email, SECRET_KEY)
        r.phone = xor_encrypt(data.phone, SECRET_KEY)
        r.address = xor_encrypt(data.address, SECRET_KEY)
        r.gender = data.gender

        db.commit()
        db.refresh(r)
        return r

    @staticmethod
    def delete(db: Session, id: int):
        r = BiodataRepository.get_by_id(db, id)
        if not r:
            return False
        BiodataRepository.delete(db, r)
        return True