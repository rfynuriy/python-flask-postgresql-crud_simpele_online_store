from flask import jsonify, request, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import select
from marshmallow import ValidationError

from app.models import Users, Products
from app.extensions import db
from app.schemas import AddProductSchema

products_bp = Blueprint('products', __name__)

@products_bp.route("/add/product", methods=["POST"])
@jwt_required()
def add_product():
    current_user_id = get_jwt_identity()
    current_user = db.session.get(Users, current_user_id)
    current_user_role = current_user.role.name

    if current_user_role != "SELLER":
        return jsonify({"message": "You are not a seller"}), 403

    data = request.get_json()
    try:
        clean = AddProductSchema().load(data)
    except ValidationError as error:
        return jsonify(error.messages), 400

    product_name = clean["product_name"]
    price = clean["price"]
    stok = clean["stok"]
    description = clean["description"]

    results = Products(
        seller_id=current_user_id,
        product_name=product_name,
        price=price,
        stok=stok,
        description=description
        )
    db.session.add(results)
    db.session.commit()
    return jsonify({"message":"Product successfully added.",
                    "product_name":product_name,
                    "price":price,
                    "stok":stok,
                    "description":description
                    })

@products_bp.route("/view/products", methods=["GET"])
def view_products():
    retrieve_product_data = db.session.scalars(select(Products)).all()
    results = []
    for i in retrieve_product_data:
        results.append({
            "seller": i.seller_products.username,
            "product_name": i.product_name,
            "price": i.price,
            "stok": i.stok,
            "description": i.description
        })
    return jsonify(results)