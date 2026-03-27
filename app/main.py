import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
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


@app.get("/", response_class=HTMLResponse)
def root():
    html_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    with open(html_path) as f:
        return f.read()


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
def list_api_resources(
    search: str | None = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    """
    Return API resources with optional search and pagination.

    - **search**: filter by name, description, or URL (case-insensitive)
    - **skip**: number of records to skip (for pagination)
    - **limit**: max records to return (default 20, max 100)
    """
    limit = min(limit, 100)
    query = db.query(database.APIResource)
    if search:
        term = f"%{search}%"
        query = query.filter(
            database.APIResource.name.ilike(term)
            | database.APIResource.description.ilike(term)
            | database.APIResource.url.ilike(term)
        )
    return query.order_by(database.APIResource.id).offset(skip).limit(limit).all()


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
