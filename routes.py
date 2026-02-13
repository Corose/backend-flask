from flask import Blueprint, request, jsonify
from models import db, User

api = Blueprint("api", __name__)

@api.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

@api.route("/users", methods=["POST"])
def create_user():
    data = request.json
    user = User(
        nombre=data.get("nombre"),
        usuario=data.get("usuario"),
        correo=data.get("correo"),
        equipo_trabajo=data.get("equipo_trabajo"),
        jefe_directo=data.get("jefe_directo"),
        accesos=data.get("accesos", []),
        comentarios=data.get("comentarios", "")
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Usuario creado"}), 201
