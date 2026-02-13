from flask import Flask
from extensions import db
from routes import api

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///okai.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.register_blueprint(api, url_prefix="/api")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

@app.route("/")
def home():
    return {"status": "ok", "service": "backend-flask"}
