from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token
from sqlalchemy import select

from app.extensions import db, bcrypt
from app.models import Users


auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data["username"]
    email = data["email"]
    before_pw_hash = data["password_hash"]
    phone_number = data["phone_number"]
    after_pw_hash = bcrypt.generate_password_hash(before_pw_hash).decode("utf-8")
    results = Users(
        username=username,
        email=email,
        password_hash=after_pw_hash,
        phone_number=phone_number
        )
    db.session.add(results)
    db.session.commit()
    return jsonify({"message": "User JSON data successfully saved!"})

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    raw_password = data["password"]

    user = db.session.scalar(select(Users).filter_by(username=username))
    if not user:
        return jsonify({"message": "Incorrect username or password"}), 401
    if bcrypt.check_password_hash(user.password_hash, raw_password):
        user_id_string = str(user.id) # identity
        custom_claims = {"role" : user.role.name} # yang dibawa oleh identity
        access_token = create_access_token(identity=user_id_string, additional_claims=custom_claims)
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"message": "Incorrect username or password"}), 401