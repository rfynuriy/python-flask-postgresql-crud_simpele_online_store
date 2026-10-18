from flask import jsonify, request, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models import Users, UserRole
from app.extensions import db

users_bp = Blueprint('users', __name__)

@users_bp.route("/change/role/<int:Target_ID>", methods=["PUT"])
@jwt_required()
def role_change(Target_ID):
    current_user_id = get_jwt_identity() # ambil identity (hanya id yang ada disini)
    current_user = db.session.get(Users, current_user_id)
    current_user_role = current_user.role.name

    target = db.session.get(Users, Target_ID)
    if not target:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    input_role = data["role"].upper()

    if input_role == "ADMIN" and current_user_role != "ADMIN":
        return jsonify({"message": "You do not have the right to this."}), 403
    if int(current_user_id) != Target_ID and current_user_role != "ADMIN":
        return jsonify({"message": "You do not have the right to change another user's role."}), 403

    try:
        enum_restrictions = UserRole[input_role]
        target.role = enum_restrictions
        db.session.commit()

        if input_role == "CUSTOMER":
            return jsonify({"message" : "success!", "target": Target_ID, "role":"customer"})
        if input_role == "SELLER":
            return jsonify({"message" : "success!", "target": Target_ID, "role":"seller"})
        else:
            return jsonify({"message" : "success!", "target": Target_ID, "role":"admin"})
    except KeyError:
        return jsonify({"message" : "You have to type 'SELLER' or 'CUSTOMER'."}), 400