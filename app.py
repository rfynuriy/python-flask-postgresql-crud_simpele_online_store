#Flask
from flask import Flask, request, jsonify

#sql alchemy basic
from sqlalchemy import select

#JWT
from flask_jwt_extended import get_jwt_identity, jwt_required

from config import DevelopmentConfig
from extensions import bcrypt, db, migrate, jwt
from models import Users, UserRole, Products, Orders, ProductsOrders
from schemas import CheckoutSchema
from errors import InsufficientStockError

from routes import auth_bp, users_bp

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
bcrypt.init_app(app)
db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(users_bp, url_prefix='/users')

@app.route("/add/product", methods=["POST"])
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
        price=float(price),
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

@app.route("/view/products", methods=["GET"])
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

@app.route("/checkout", methods=["POST"])
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

@app.route("/my/order", methods=["GET"])
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


if __name__ == '__main__':
    app.run(debug=True)