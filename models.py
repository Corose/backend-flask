from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    equipo = db.Column(db.String(50), nullable=False)
    jefe = db.Column(db.String(100))
    accesos = db.Column(db.Text)
    comentarios = db.Column(db.Text)
