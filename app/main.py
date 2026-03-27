from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import database, schemas

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="API Library Manager")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Welcome to the API Library Manager!"}

@app.post("/api/", response_model=schemas.APIResourceOut)
def create_api_resource(resource: schemas.APIResourceCreate, db: Session = Depends(get_db)):
    db_resource = database.APIResource(**resource.dict())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

@app.get("/api/", response_model=list[schemas.APIResourceOut])
def list_api_resources(db: Session = Depends(get_db)):
    return db.query(database.APIResource).all()
