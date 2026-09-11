#Flask
from flask import Flask, request, jsonify

#sql alchemy basic
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as SQLEnum

#enum
from enum import Enum

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

class UserRole(Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    SELLER = "seller"

class Users(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(700), unique=True)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole, name="user_role_enum"), default=UserRole.CUSTOMER)