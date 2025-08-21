# from fastapi import FastAPI, HTTPException, Depends
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
# from typing import List
# from . import models, schemas, auth

# from models import Base, Todo
# from database import engine, SessionLocal

# # Create tables
# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# # Dependency to get DB session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# # User Registration
# @app.post("/register", response_model=schemas.User)
# def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     # Check if username or email already exists
#     db_user = db.query(models.User).filter(
#         (models.User.username == user.username) | (models.User.email == user.email)
#     ).first()
#     if db_user:
#         raise HTTPException(status_code=400, detail="Username or email already registered")
#     # Hash the password
#     hashed_password = auth.hash_password(user.password)
#     # Create new user
#     db_user = models.User(
#         username=user.username,
#         email=user.email,
#         hashed_password=hashed_password
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# # User Login
# @app.post("/login")
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.username == form_data.username).first()
#     if not user or not auth.verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     token = auth.create_access_token({"sub": user.username})
#     return {"access_token": token, "token_type": "bearer"}







# # --- CRUD Endpoints ---

# # POST /todos → Add a new todo
# @app.post("/todos", response_model=dict)
# def create_todo(task: str, db: Session = Depends(get_db)):
#     new_todo = Todo(task=task)
#     db.add(new_todo)
#     db.commit()
#     db.refresh(new_todo)
#     return {"id": new_todo.id, "task": new_todo.task, "done": new_todo.done}

# # GET /todos → Fetch all todos
# @app.get("/todos", response_model=List[dict])
# def get_todos(db: Session = Depends(get_db)):
#     todos = db.query(Todo).all()
#     return [{"id": t.id, "task": t.task, "done": t.done} for t in todos]

# # PUT /todos/{id} → Update todo
# @app.put("/todos/{id}", response_model=dict)
# def update_todo(id: int, task: str = None, done: bool = None, db: Session = Depends(get_db)):
#     todo = db.query(Todo).filter(Todo.id == id).first()
#     if not todo:
#         raise HTTPException(status_code=404, detail="Todo not found")
#     if task is not None:
#         todo.task = task
#     if done is not None:
#         todo.done = done
#     db.commit()
#     db.refresh(todo)
#     return {"id": todo.id, "task": todo.task, "done": todo.done}

# # DELETE /todos/{id} → Delete todo
# @app.delete("/todos/{id}", response_model=dict)
# def delete_todo(id: int, db: Session = Depends(get_db)):
#     todo = db.query(Todo).filter(Todo.id == id).first()
#     if not todo:
#         raise HTTPException(status_code=404, detail="Todo not found")
#     db.delete(todo)
#     db.commit()
#     return {"message": f"Todo with id {id} deleted successfully"}


from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import Base, engine, get_db
import models, schemas
from  auth import hash_password, verify_password, create_access_token, decode_token
 
# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="JWT-Protected To-Do API")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exc
    except Exception:
        raise credentials_exc
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise credentials_exc
    return user

# -------- Auth --------
@app.post("/register", response_model=schemas.UserOut, status_code=201)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # Uniqueness checks
    if db.query(models.User).filter(models.User.username == user_in.username).first():
        raise HTTPException(400, "Username already exists")
    if db.query(models.User).filter(models.User.email == user_in.email).first():
        raise HTTPException(400, "Email already exists")

    user = models.User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me", response_model=schemas.UserOut)
def read_me(current_user: models.User = Depends(get_current_user)):
    return current_user

# -------- Todos (secured) --------
@app.get("/todos", response_model=list[schemas.TodoOut])
def list_todos(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Todo).filter(models.Todo.owner_id == current_user.id).all()

@app.post("/todos", response_model=schemas.TodoOut, status_code=201)
def create_todo(
    todo_in: schemas.TodoCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    todo = models.Todo(task=todo_in.task, done=todo_in.done, owner_id=current_user.id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

@app.get("/todos/{todo_id}", response_model=schemas.TodoOut)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    todo = db.query(models.Todo).filter(
        models.Todo.id == todo_id, models.Todo.owner_id == current_user.id
    ).first()
    if not todo:
        raise HTTPException(404, "Todo not found")
    return todo

@app.patch("/todos/{todo_id}", response_model=schemas.TodoOut)
def update_todo(
    todo_id: int,
    todo_in: schemas.TodoUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    todo = db.query(models.Todo).filter(
        models.Todo.id == todo_id, models.Todo.owner_id == current_user.id
    ).first()
    if not todo:
        raise HTTPException(404, "Todo not found")
    if todo_in.task is not None:
        todo.task = todo_in.task
    if todo_in.done is not None:
        todo.done = todo_in.done
    db.commit()
    db.refresh(todo)
    return todo

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    todo = db.query(models.Todo).filter(
        models.Todo.id == todo_id, models.Todo.owner_id == current_user.id
    ).first()
    if not todo:
        raise HTTPException(404, "Todo not found")
    db.delete(todo)
    db.commit()
    return None
