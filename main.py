from fastapi import FastAPI,Depends,HTTPException,Query
from pydantic import BaseModel
from typing import List,Annotated,Optional
import models
from sqlalchemy.orm import Session
from database import engine,SessionLocal,Base


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/full_parking_space_list')
async def parking_space_list(db: Session = Depends(get_db)):
    parking_spaces = db.query(models.Parking_Space_List).order_by(models.Parking_Space_List.space_id).all()
    return parking_spaces

@app.put('/parking_sapce_list/update/{id}')
async def update_parking_space_list(id:str,db: Session = Depends(get_db)):
    space=db.query(models.Parking_Space_List).filter(models.Parking_Space_List.space_id==id).first()
    if not space:
        raise HTTPException(status_code=404, detail="Parking space not found")

    if space.Availbility_status == "Vacant":
        space.Availbility_status = "Occupied"
    elif space.Availbility_status == "Occupied":
        space.Availbility_status = "Vacant"
    else:
        raise HTTPException(status_code=400, detail="Invalid availability status")

    db.commit()
    db.refresh(space)
    return space


@app.get("/empty_parking_list")
async def empty_parking_list(
    level: Optional[int] = Query(default=None),
    db: Session = Depends(get_db)
):
    # Start with base query (not executing anything yet)
    query = db.query(models.Parking_Space_List).filter(
        models.Parking_Space_List.Availbility_status == "Vacant"
    )

    # Only add level filter if it's provided
    if level is not None:
        query = query.filter(models.Parking_Space_List.Level == level)

    # Now apply ordering BEFORE calling `.all()`
    query = query.order_by(models.Parking_Space_List.space_id)

    # Execute the query
    empty_spaces = query.all()

    return empty_spaces


    


