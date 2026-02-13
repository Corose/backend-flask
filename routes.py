from flask import Blueprint, request, jsonify
from models import db, User

api = Blueprint("api", __name__)

@api.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])
