import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# Load .env
load_dotenv()

app = Flask(__name__)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

# Init DB
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models
from models import *

# Import routes (this will register your HTML pages)
import routes

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
