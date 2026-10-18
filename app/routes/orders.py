from flask import jsonify, request, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import select

from app.models import Orders, Products, ProductsOrders
from app.extensions import db
from app.schemas import CheckoutSchema
from app.errors import InsufficientStockError

orders_bp = Blueprint('orders', __name__)

@orders_bp.route("/checkout", methods=["POST"])
@jwt_required()
def checkout():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    schema= CheckoutSchema()
    error= schema.validate(data)
    if error:
        return jsonify(error), 400
    items = data["items"]

    try:
        new_order = Orders(user_id=current_user_id)
        db.session.add(new_order)

        db.session.flush()

        for item in items:
            products_id = item["products_id"]
            quantity = item["quantity"]

            product = db.session.get(Products, products_id)
            if not product:
                raise Exception(f"Product with ID {products_id} was not found.")
            if product.stok < quantity:
                raise InsufficientStockError("I apologize, but there is insufficient stock.")

            product.stok = product.stok-quantity

            detail_order = ProductsOrders(
                orders_id= new_order.id,
                products_id= product.id,
                purchase_quantity= quantity,
                purchase_price= float(product.price)
            )
            db.session.add(detail_order)

        db.session.commit()
        return jsonify({
            "message": "Checkout berhasil!",
            "order_id": new_order.id,
            "detail_order": items
            }), 200

    except InsufficientStockError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@orders_bp.route("/my/order", methods=["GET"])
@jwt_required()
def order_history():
    current_user_id = get_jwt_identity()
    statement =select(Orders).filter_by(user_id=current_user_id).order_by(Orders.created_at.desc())
    user_orders= db.session.scalars(statement).all()

    orders_data= []
    for order in user_orders:
        items_list = []
        for item in order.products_order:
            items_list.append({
                "products_name": item.list_products.product_name,
                "quantity": item.purchase_quantity,
                "price": float(item.purchase_price),
                "subtotal": float(item.purchase_quantity * item.purchase_price)
            })

        total_price_order= sum(item["subtotal"] for item in items_list)
        orders_data.append({
            "order_id": order.id,
            "order_status": order.status.name,
            "created_at": order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "total_items": len(items_list),
            "total_price": total_price_order,
            "items": items_list
        })

    return jsonify({
        "message": "success",
        "orders_quantity": len(user_orders),
        "my_orders": orders_data
    })
