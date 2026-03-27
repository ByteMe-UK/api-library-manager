from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import database, schemas

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="API Library Manager",
    description="A catalogue for saving and managing REST API resources.",
    version="1.0.0",
)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "message": "Welcome to the API Library Manager!",
        "docs": "/docs",
        "endpoints": {
            "list": "GET /api/",
            "create": "POST /api/",
            "get": "GET /api/{id}",
            "update": "PUT /api/{id}",
            "delete": "DELETE /api/{id}",
        },
    }


@app.post("/api/", response_model=schemas.APIResourceOut, status_code=201)
def create_api_resource(resource: schemas.APIResourceCreate, db: Session = Depends(get_db)):
    """Add a new API resource to the library."""
    existing = db.query(database.APIResource).filter(
        database.APIResource.url == resource.url
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="A resource with this URL already exists.")
    db_resource = database.APIResource(**resource.model_dump())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource


@app.get("/api/", response_model=list[schemas.APIResourceOut])
def list_api_resources(db: Session = Depends(get_db)):
    """Return all API resources."""
    return db.query(database.APIResource).all()


@app.get("/api/{resource_id}", response_model=schemas.APIResourceOut)
def get_api_resource(resource_id: int, db: Session = Depends(get_db)):
    """Get a single API resource by ID."""
    resource = db.query(database.APIResource).filter(
        database.APIResource.id == resource_id
    ).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found.")
    return resource


@app.put("/api/{resource_id}", response_model=schemas.APIResourceOut)
def update_api_resource(
    resource_id: int,
    updates: schemas.APIResourceUpdate,
    db: Session = Depends(get_db),
):
    """Update one or more fields on an existing resource."""
    resource = db.query(database.APIResource).filter(
        database.APIResource.id == resource_id
    ).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found.")
    changed = updates.model_dump(exclude_unset=True)
    for field, value in changed.items():
        setattr(resource, field, value)
    db.commit()
    db.refresh(resource)
    return resource


@app.delete("/api/{resource_id}", status_code=204)
def delete_api_resource(resource_id: int, db: Session = Depends(get_db)):
    """Delete an API resource by ID."""
    resource = db.query(database.APIResource).filter(
        database.APIResource.id == resource_id
    ).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found.")
    db.delete(resource)
    db.commit()
