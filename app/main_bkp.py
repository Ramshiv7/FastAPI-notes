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

# Create Dependency with DataBase Models




class Puppies(BaseModel):
    name: str
    age: int
    breed: str
    vaccinated: bool = True
    special_need: Optional[str] = None


# Store POST in a Memory

my_posts = [ {"name": "tommy","age": 5, "breed":"lab", "id":1},
{"name":"gun", "age":3, "breed":"pitbull", "id":2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index(id):
    for i, j in enumerate(my_posts):
        if j['id'] == id:
            print(i, j)
            return i


@app.get('/pups')
async def home():
    return {"Greeting" : my_posts}


@app.get('/pups/{id}')
async def get_pup_id(id: int, response: Response):
    find_pup = find_post(id)
    if not find_pup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No data found for the {id}')
       # response.status_code = status.HTTP_404_NOT_FOUND
       # return {"data": f"No data found for the {id}"}

    return {"data": find_pup}


"""
@app.get('/pups')
async def get_pups():
    return


@app.post('/donate-pups/')
async def donate_pusp(pup_details: dict = Body(...)):
    print(pup_details)
    for _ in pup_details:
        return {f'pup_details' :{ f'id: {pup_details[_]}'}}

"""

@app.post('/newpups', status_code=status.HTTP_201_CREATED)
async def send_for_adopt(new_pup: PupHub, db: Session = Depends(get_db)):
    new_data = models.PupHub(name = new_pup.name, age=new_pup.age, breed=new_pup.breed)
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    #print(new_pup)
    #print(new_pup.dict())
    #new_posts = new_pup.dict()
    #new_posts['id'] = randrange(0,1000000)
    #my_posts.append(new_posts)
    return {"data": new_data}



@app.delete('/pups/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_pup(id: int):
    # implement delete by index since - my_posts defined as list
    index = find_index(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/pups/{id}')
async def update_pup(id: int, up_req: Puppies):
    req_dict = up_req.dict()

    index = find_index(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    req_dict['id'] = id
    my_posts[index] = req_dict
    return {"data": req_dict}



# Testing Database Creation

@app.get('/')
async def db_connet(db: Session = Depends(get_db)):
    # Retrieve Data from Backend and Send it to Frontend
    pups = db.query(models.PupHub).all()
    return {"Data": pups}