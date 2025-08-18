# from sqlalchemy.orm import Session
# from . import models, schemas
# from typing import List, Optional

# def get_todo(db: Session, todo_id: int) -> Optional[models.Todo]:
#     return db.query(models.Todo).filter(models.Todo.id == todo_id).first()

# def get_todos(db: Session) -> List[models.Todo]:
#     return db.query(models.Todo).all()

# def create_todo(db: Session, todo: schemas.TodoCreate) -> models.Todo:
#     db_todo = models.Todo(task=todo.task, done=todo.done)
#     db.add(db_todo)
#     db.commit()
#     db.refresh(db_todo)
#     return db_todo

# def update_todo(db: Session, todo_id: int, todo_in: schemas.TodoUpdate) -> Optional[models.Todo]:
#     db_todo = get_todo(db, todo_id)
#     if not db_todo:
#         return None
#     if todo_in.task is not None:
#         db_todo.task = todo_in.task
#     if todo_in.done is not None:
#         db_todo.done = todo_in.done
#     db.commit()
#     db.refresh(db_todo)
#     return db_todo

# def delete_todo(db: Session, todo_id: int) -> bool:
#     db_todo = get_todo(db, todo_id)
#     if not db_todo:
#         return False
#     db.delete(db_todo)
#     db.commit()
#     return True
