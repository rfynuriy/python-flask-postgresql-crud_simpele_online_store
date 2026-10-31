from flask import jsonify, request, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import select

from app.models import Users, Products
from app.extensions import db

from decimal import Decimal

products_bp = Blueprint('products', __name__)

@products_bp.route("/add/product", methods=["POST"])
@jwt_required()
def add_product():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    current_user = db.session.get(Users, current_user_id)
    current_user_role = current_user.role.name

    if current_user_role != "SELLER":
        return jsonify({"message": "You are not a seller"}), 403

    product_name = data["product_name"]
    price = data["price"]
    stok = data["stok"]
    description = data.get("description")

    results = Products(
        seller_id=current_user_id,
        product_name=product_name,
        price=Decimal(str(price)),
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