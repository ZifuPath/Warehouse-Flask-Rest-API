from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
DB_NAME = "database.db"

def create_database(app):
    if not path.exists(DB_NAME):
        db.create_all(app=app)
        print('Created Database!')


app = Flask(__name__)

app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']=False
db = SQLAlchemy(app)
create_database(app)



