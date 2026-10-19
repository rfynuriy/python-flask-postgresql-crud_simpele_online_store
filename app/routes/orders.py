from flask import jsonify, request, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import select

from app.models import Orders
from app.extensions import db
from app.schemas import CheckoutSchema
from app.errors import InsufficientStockError, ProductNotFoundError
from app.services import create_order

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
        order = create_order(current_user_id, items)
        return jsonify({
            "message": "Checkout berhasil!",
            "order_id": order.id,
            "detail_order": items
            }), 200

    except ProductNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except InsufficientStockError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
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
