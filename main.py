#from http.client import HTTPException
from typing import Optional
from xmlrpc.client import boolean

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

import models
from database import Base, SessionLocal, engine

app=FastAPI()
models.Base.metadata.create_all(bind=engine)
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Todo(BaseModel):
    title : str
    description : Optional[str]
    priority : int = Field(gt=0, lt=6, description='priority must be between 1 and 5')
    complete : bool


@app.get('/')
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()



@app.get('/todo/{to_do}')
async def read_todo(todo_id:int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise http_exception()


@app.post('/')
async def create_todo(todo: Todo, db: Session = Depends(get_db)):
    todo_model = models.Todos()
    todo_model.title = todo.title 
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    
    db.add(todo_model)
    db.commit()
    return successful_response(201)
    

@app.put('/{todo_id}')
async def update_todo(todo_id :int, todo: Todo, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo_model is None:
        raise http_exception(200)
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    db.add(todo_model)
    db.commit()
    return successful_response()
    
@app.delete('/{todo_id')
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo_model is None:
        raise http_exception()
    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
    db.commit()
    return successful_response(200)

def successful_response (status_code:int):
    return {
        'status': status_code,
        'transacation': 'Succesful'
    }
def http_exception():
    raise HTTPException(status_code=404, detail="Todo not found")
