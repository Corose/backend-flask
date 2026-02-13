
from flask import Blueprint, request, jsonify, session
from app import db
from models import User, Acceso, Comentario, Auth
from flask_bcrypt import Bcrypt
import requests, os

api = Blueprint("api", __name__, url_prefix="/api")
bcrypt = Bcrypt()

def notify_teams(usuario):
    url = os.getenv("TEAMS_WEBHOOK_URL")
    if not url: return
    requests.post(url, json={"text": f"🆕 Nuevo usuario agregado por invitado: {usuario}"})

@api.route("/auth/register", methods=["POST"])
def register():
    data = request.json
    pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    db.session.add(Auth(username=data["username"], password_hash=pw, role=data.get("role","admin")))
    db.session.commit()
    return jsonify(ok=True)

@api.route("/auth/login", methods=["POST"])
def login():
    data = request.json
    u = Auth.query.filter_by(username=data["username"]).first()
    if u and bcrypt.check_password_hash(u.password_hash, data["password"]):
        session["user"]=u.username; session["role"]=u.role
        return jsonify(ok=True, role=u.role)
    return jsonify(ok=False),401

@api.route("/users", methods=["GET"])
def users():
    rows = User.query.all()
    return jsonify([{"id":u.id,"nombre":u.nombre,"usuario":u.usuario,"correo":u.correo,"equipo":u.equipo,"jefe_directo":u.jefe_directo} for u in rows])

@api.route("/users", methods=["POST"])
def add_user():
    data = request.json
    u = User(**data.get("user",{}))
    db.session.add(u); db.session.commit()
    acc = data.get("accesos")
    if acc:
        db.session.add(Acceso(user_id=u.id, **acc)); db.session.commit()
    if session.get("role")=="invitado":
        notify_teams(u.usuario)
    return jsonify(ok=True)

@api.route("/users/<int:uid>", methods=["PUT"])
def update_user(uid):
    if session.get("role")!="admin": return jsonify(error="forbidden"),403
    data = request.json
    u = User.query.get_or_404(uid)
    for k,v in data.get("user",{}).items(): setattr(u,k,v)
    db.session.commit()
    return jsonify(ok=True)

@api.route("/users/<int:uid>", methods=["DELETE"])
def delete_user(uid):
    if session.get("role")!="admin": return jsonify(error="forbidden"),403
    u = User.query.get_or_404(uid)
    db.session.delete(u); db.session.commit()
    return jsonify(ok=True)

@api.route("/comentarios/<int:uid>", methods=["POST"])
def add_comment(uid):
    db.session.add(Comentario(user_id=uid, comentario=request.json["comentario"]))
    db.session.commit()
    return jsonify(ok=True)
