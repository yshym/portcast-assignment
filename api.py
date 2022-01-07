from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from database import get_db
from database.models import Container, BOL


app = FastAPI()


@app.get("/containers", response_model=List[Container])
def read_containers(db: Session = Depends(get_db)):
    return list(db.exec(select(Container)))


@app.get("/containers/{number}", response_model=Container)
def read_container(number: str, db: Session = Depends(get_db)):
    container = db.get(Container, number)
    if not container:
        raise HTTPException(status_code=404, detail="container not found")
    return container


@app.get("/bols", response_model=List[Container])
def read_bols(db: Session = Depends(get_db)):
    return list(db.exec(select(BOL)))


@app.get("/bols/{number}", response_model=Container)
def read_bol(number: str, db: Session = Depends(get_db)):
    container = db.get(BOL, number)
    if not container:
        raise HTTPException(status_code=404, detail="container not found")
    return container
