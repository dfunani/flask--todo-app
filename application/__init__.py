import os
from sqlalchemy import URL
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = URL.create(
    os.environ['TYPE'],
    username=os.environ['USERNAME'],
    password=os.environ['PASSWORD'],  # plain (unescaped) text
    host=os.environ['HOST'],
    database=os.environ["DATABASE"],
)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

db = SQLAlchemy(app)