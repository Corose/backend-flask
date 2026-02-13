from flask import Blueprint, request, jsonify
from extensions import db
from models import User

routes = Blueprint("routes", __name__)

@routes.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([
        {
            "id": u.id,
            "nombre": u.nombre,
            "usuario": u.usuario,
            "correo": u.correo,
            "equipo": u.equipo,
            "jefe": u.jefe,
            "accesos": u.accesos,
            "comentarios": u.comentarios
        } for u in users
    ])

@routes.route("/api/users", methods=["POST"])
def create_user():
    data = request.json
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "Usuario creado"})
