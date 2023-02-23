from flask import Flask,Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os 
from flask_login import LoginManager
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] =  "asjdoajsdojas"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ma= Marshmallow(app)

db = SQLAlchemy(app)
Migrate(app,db)
login_manager = LoginManager(app)
login_manager.login_view = 'admin.Login'

from application.main.routes import main
app.register_blueprint(main)
from application.admin.routes import admin
app.register_blueprint(admin)