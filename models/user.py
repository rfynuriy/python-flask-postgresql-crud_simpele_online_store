from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum as SQLEnum

from enum import Enum

from extensions import db

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .products import Products
    from .orders import Orders

# ============================= ENUM ==================================
class UserRole(Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    SELLER = "seller"

# ============================= MODELS ================================
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