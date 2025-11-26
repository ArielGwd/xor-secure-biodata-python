from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request

from app.controllers.biodata_controller import router as biodata_router
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/client/static"), name="static")
view = Jinja2Templates(directory="app/client/views")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return view.TemplateResponse("index.html", {"request": request})


app.include_router(biodata_router)