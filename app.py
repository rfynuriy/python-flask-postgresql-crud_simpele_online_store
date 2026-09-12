#Flask
from flask import Flask, request, jsonify

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
from flask_migrate import migrate

#JWT
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

#Marshmallow
from flask_marshmallow import Marshmallow

#.env
import os
from decimal import Decimal
from dotenv import load_dotenv


app = Flask(__name__)

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
migrate = migrate(app, db)

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

    orders_list: Mapped[list["Orders"]] = relationship(back_populates="user")

class Products(db.Model):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2), nullable=False)
    stok: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String(1000))

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