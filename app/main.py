from fastapi import FastAPI

from app.controllers.biodata_controller import router as biodata_router
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(biodata_router)
