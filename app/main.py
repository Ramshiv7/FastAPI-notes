from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from sqlalchemy.orm import Session

from . import models
from .database import engine, SessionLocal, get_db
#from models import PupHub


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Pydantic Model - Important ( To Model & Validate the Input from API )
class Puppies(BaseModel):
    name: str
    age: int
    breed: str
    for_sale: bool = True


# Get all Pup data
@app.get('/pups')
async def show_pups(db: Session = Depends(get_db)):
    return_data = db.query(models.PupHub).all()
    return {"data": return_data }


# Get the Pup Data By ID
@app.get('/pups/{id}', status_code=status.HTTP_404_NOT_FOUND)
async def get_pup_by_id(id: int,db: Session = Depends(get_db)):
    # .first() & .all() -> if only one result -> .first() , if still want postgres to look for other id=1 then .all()
    x = db.query(models.PupHub).filter(models.PupHub.id == id).all()
    return {"data" : x}


# Create a PoST - Insert data into Postgres DataBase
@app.post('/pups', status_code=status.HTTP_201_CREATED)
async def create_pup_data(pups_data: Puppies, db: Session = Depends(get_db)):
    #print(**pups_data.dict())
    new_pup = models.PupHub(**pups_data.dict()) # Achieve Dict Unpacking - Help with All Columns field match with Database
   # new_pup = models.PupHub(name=pups_data.name, age=pups_data.age, breed=pups_data.breed) -- Inefficient if we have 50 fields in the table
    db.add(new_pup)
    db.commit()
    db.refresh(new_pup)

    return {"data": new_pup}

# Delete a PoSt by ID 
@app.delete('/pups/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_pup_data(id: int, db: Session=Depends(get_db)):
    del_query = db.query(models.PupHub).filter(models.PupHub.id == id)

    if del_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Pup with ID: {id} Does not exist')


    del_query.delete(synchronize_session=False)

    db.commit()


# Update a PoSt by ID
@app.put('/pups/{id}')
async def update_pup_data(id: int,pups_data: Puppies, db: Session=Depends(get_db)):
    update_q = db.query(models.PupHub).filter(models.PupHub.id == id)

    # if not exists
    update_query = update_q.first()

    if update_query == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Pup with ID: {id} does not exist')

    update_q.update(pups_data.dict(),synchronize_session=False)

    db.commit()
    return {"data": update_q.first()}

