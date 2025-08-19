from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from models import Base, Todo
from database import engine, SessionLocal

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- CRUD Endpoints ---

# POST /todos → Add a new todo
@app.post("/todos", response_model=dict)
def create_todo(task: str, db: Session = Depends(get_db)):
    new_todo = Todo(task=task)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return {"id": new_todo.id, "task": new_todo.task, "done": new_todo.done}

# GET /todos → Fetch all todos
@app.get("/todos", response_model=List[dict])
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return [{"id": t.id, "task": t.task, "done": t.done} for t in todos]

# PUT /todos/{id} → Update todo
@app.put("/todos/{id}", response_model=dict)
def update_todo(id: int, task: str = None, done: bool = None, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if task is not None:
        todo.task = task
    if done is not None:
        todo.done = done
    db.commit()
    db.refresh(todo)
    return {"id": todo.id, "task": todo.task, "done": todo.done}

# DELETE /todos/{id} → Delete todo
@app.delete("/todos/{id}", response_model=dict)
def delete_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": f"Todo with id {id} deleted successfully"}
