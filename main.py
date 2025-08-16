from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()
todos=[]
class TodosItem(BaseModel):
    id:int
    task:str
    done:bool

@app.get("/todos")
def get_todos():
    return todos

@app.post("/todos")
def add_todo(todo:TodosItem):
    todos.append(todo)
    return todo

@app.put("/todos/{id}")
def update_todo(id:int,todo:TodosItem):
    for i,t in enumerate(todos):
        if t.id == id:
            todos[i]=todo
            return todo
    return {"error":"todo not found"}


@app.delete("/todos/{id}")
def delete_todo(id:int):
    for i,t in enumerate(todos):
        if t.id == id:
            todos.pop(i)
            return{"message":"deleted successfully"}
    return{"error":"todo not found"}