#Flask
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt

#sql alchemy basic
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum

#enum
from enum import Enum

# timestamp for [created_at], [updated_at]
from datetime import datetime
from sqlalchemy import func

#Flask_migrate
from flask_migrate import Migrate

#JWT
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, get_jwt

#Marshmallow
from flask_marshmallow import Marshmallow

#.env
import os
from decimal import Decimal
from dotenv import load_dotenv


app = Flask(__name__)
bcrypt = Bcrypt(app)

load_dotenv()
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_secret_key = os.getenv("SECRET_KEY")

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SECRET_KEY'] = db_secret_key

db = SQLAlchemy(app)
migrate = Migrate(app, db)
#instalasi jwt
app.config["JWT_SECRET_KEY"] = db_secret_key
jwt = JWTManager(app)

class UserRole(Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    SELLER = "seller"

class StatusOrder(Enum):
    PENDING = "pending"
    PAID = "paid"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class Users(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(700), unique=True)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole, name="user_role_enum"), default=UserRole.CUSTOMER)

    list_products_seller: Mapped[list["Products"]] = relationship(back_populates="seller_products")
    orders_list: Mapped[list["Orders"]] = relationship(back_populates="user")

class Products(db.Model):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2), nullable=False)
    stok: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)

    seller_products: Mapped["Users"] = relationship(back_populates="list_products_seller")
    products_list: Mapped[list["ProductsOrders"]] = relationship(back_populates="list_products")

class Orders(db.Model):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    status: Mapped[StatusOrder] = mapped_column(SQLEnum(StatusOrder, name="Status_Order_enum"), default=StatusOrder.PENDING)

    user: Mapped["Users"] = relationship(back_populates="orders_list")
    products_order: Mapped[list["ProductsOrders"]] = relationship(back_populates="orders_items")

class ProductsOrders(db.Model):
    __tablename__ = "products_orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    orders_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    products_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    purchase_quantity: Mapped[int] = mapped_column(nullable=False)
    purchase_price: Mapped[Decimal]  = mapped_column(Numeric(precision=10, scale=2), nullable=False)

    orders_items : Mapped["Orders"] = relationship(back_populates="products_order")
    list_products: Mapped["Products"] = relationship(back_populates="products_list")

@app.route("/register", methods=["POST"])
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

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    raw_password = data["password"]

    user = Users.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "Incorrect username or password"}), 401
    if bcrypt.check_password_hash(user.password_hash, raw_password):
        user_id_string = str(user.id) # identity
        custom_claims = {"role" : user.role.name} # yang dibawa oleh identity
        access_token = create_access_token(identity=user_id_string, additional_claims=custom_claims)
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"message": "Incorrect username or password"}), 401

@app.route("/change/role/<int:Target_ID>", methods=["PUT"])
@jwt_required()
def role_change(Target_ID):
    current_user_id = get_jwt_identity() # ambil identity (hanya id yang ada disini)
    current_user = Users.query.get(current_user_id)
    current_user_role = current_user.role.name

    target = Users.query.get(Target_ID)
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

@app.route("/add/product", methods=["POST"])
@jwt_required()
def add_product():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    current_user = Users.query.get(current_user_id)
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
    retrieve_product_data = Products.query.all()
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

class InsufficientStockError(Exception):
    pass
@app.route("/checkout", methods=["POST"])
@jwt_required()
def checkout():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    items = data["items"]

    try:
        new_order = Orders(user_id=current_user_id)
        db.session.add(new_order)

        db.session.flush()

        for item in items:
            products_id = item["products_id"]
            quantity = item["quantity"]

            product = Products.query.get(products_id)
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

@app.route("/View/My/Order/History", methods=["GET"])
@jwt_required()
def order_history():
    current_user_id = get_jwt_identity()
    user_orders= Orders.query.filter_by(user_id=current_user_id).order_by(Orders.created_at.desc()).all()

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