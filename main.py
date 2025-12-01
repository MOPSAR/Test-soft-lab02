from fastapi import FastAPI, Depends, HTTPException, status
from database import engine, get_db
from sqlalchemy.orm import Session
import schemas
import models
from typing import List

# Create all tables
models.Base.metadata.create_all(engine)


# Create new instance of FastAPI
app = FastAPI()


# Fetch all todos
@app.get("/todos/", tags=["Todos"], response_model=List[schemas.TodoResponse])
def get_todos(db: Session = Depends(get_db)):

    todos = db.query(models.Todo).all()

    if not todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No Todos at the moment try creating one",
        )

    return todos


# Fetch single todo
@app.get("/todos/{id}", tags=["Todos"], response_model=schemas.TodoResponse)
def get_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == id).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No Todo with id {id}"
        )

    return todo


# Add todo
@app.post(
    "/todos/",
    tags=["Todos"],
    response_model=schemas.TodoResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_todo(request: schemas.Todo, db: Session = Depends(get_db)):

    find_todo = db.query(models.Todo).filter(models.Todo.title == request.title).first()

    if find_todo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"This Todo already exist"
        )

    new_todo = models.Todo(title=request.title, is_complete=request.is_complete)

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


# Update todo
@app.put("/todos/{id}", tags=["Todos"], response_model=schemas.TodoResponse)
def update_todo(id: int, request: schemas.Todo, db: Session = Depends(get_db)):

    todo = db.query(models.Todo).filter(models.Todo.id == id).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="This Todo does not exist"
        )

    # Update data
    todo.title = request.title
    todo.is_complete = request.is_complete

    db.commit()
    db.refresh(todo)

    return todo


# Delete todo
@app.delete("/todos/{id}", tags=["Todos"])
def destroy_todo(id: int, request: schemas.Todo, db: Session = Depends(get_db)):

    todo = db.query(models.Todo).filter(models.Todo.id == id).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="This Todo does not exist"
        )

    # Delete todo
    db.delete(todo)

    db.commit()

    return {"message": "Todo deleted successfully"}
