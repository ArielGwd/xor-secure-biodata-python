from sqlalchemy import Column, Integer, VARCHAR, DateTime, Enum
from sqlalchemy.sql import func
from app.core.database import Base

class Biodata(Base):
    __tablename__ = "biodata"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(255), nullable=False) 
    
    email = Column(VARCHAR(1024), nullable=False)
    phone = Column(VARCHAR(1024), nullable=False)
    address = Column(VARCHAR(1024))
    
    gender = Column(Enum("male", "female", name="gender"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())