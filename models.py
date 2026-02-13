
from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120))
    usuario = db.Column(db.String(80), unique=True)
    correo = db.Column(db.String(120))
    equipo = db.Column(db.String(80))
    jefe_directo = db.Column(db.String(120))

class Acceso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    sap = db.Column(db.Boolean, default=False)
    vpn = db.Column(db.Boolean, default=False)
    helix = db.Column(db.Boolean, default=False)
    hana = db.Column(db.Boolean, default=False)
    ipc = db.Column(db.Boolean, default=False)
    gcp = db.Column(db.Boolean, default=False)
    active_directory = db.Column(db.Boolean, default=False)

class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    comentario = db.Column(db.Text)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

class Auth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(255))
    role = db.Column(db.String(20))
