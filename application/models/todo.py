from enum import Enum
import json
from .. import app, db
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

class Status(str, Enum):
    Work="Work"
    Personal="Personal"
    School="School"
    Other="Other"
    
class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    hashcode = db.Column(db.String(255), nullable=False)
    todo_id = db.relationship("Todo", backref="users", lazy=True)

    def add(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def getAll():
        result = []
        for user in db.session.execute(db.select(Users)).scalars():
            if user:
                result.append({"email": user.email, "username": user.username, "hashcode": user.hashcode })
        return result
    
    @staticmethod
    def getOne(email):
        user = Users.query.filter_by(email=email).first()
        if user:
            return {"exists": True, "user": user}
        return {"exists": False, "user": user}
    
class Todo(db.Model):
    __tablename__ = "todo"

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(Status), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def add(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def getAllForID(id):
        result = []
        for todo in Todo.query.filter_by(user_id=id):
            if todo:
                result.append({"id": todo.id, "task": todo.task, "created": todo.created, "status": (todo.status) })
        return result
    
    @staticmethod
    def delete(id):
        todo = db.session.get(Todo, id)
        db.session.delete(todo)
        db.session.commit()