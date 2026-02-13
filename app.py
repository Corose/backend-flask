import os
from flask import Flask
from extensions import db
from routes import routes

app = Flask(__name__)

database_url = os.getenv("DATABASE_URL")

if database_url:
    # Fix para SQLAlchemy con postgres
    database_url = database_url.replace("postgres://", "postgresql://")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url or "sqlite:///okai.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.register_blueprint(routes)

with app.app_context():
    db.create_all()
