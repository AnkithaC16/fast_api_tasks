# from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship

# Base = declarative_base()

# class User(Base):
#     __tablename__="users"

#     id = Column(Integer,primary_key=True,index=True)
#     username = Column(String,unique=True,index=True,nullable=False)
#     email = Column(String,unique=True,index=True,nullable=False)
#     hashed_password = Column(String,nullable=False)
#     is_active = Column(Boolean,default=True)
#     todos = relationship("todo",back_populates="owner")

# class Todo(Base):
#     __tablename__ = "todos"

#     id = Column(Integer, primary_key=True, index=True)
#     task = Column(String, nullable=False)
#     done = Column(Boolean, default=False)
#     owner_id = Column(Integer,ForeignKey("user.id"))

#     owner = relationship("User",back_populates="todos")


from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    todos = relationship("Todo", back_populates="owner")

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, nullable=False)
    done = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="todos")
