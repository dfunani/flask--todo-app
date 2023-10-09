from sqlalchemy import URL
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

url_object = URL.create(
    "postgresql",
    username="postgres",
    password="postgres",  # plain (unescaped) text
    host="192.168.0.102",
    database="strapipostgres",
)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = url_object
app.config['SECRET_KEY'] = "url_object"

db = SQLAlchemy(app)