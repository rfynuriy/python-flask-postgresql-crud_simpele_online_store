from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum,ForeignKey, func, Numeric

from datetime import datetime
from enum import Enum
from decimal import Decimal

from extensions import db

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user import Users
    from .products import Products

# ============================= ENUM ==================================
class StatusOrder(Enum):
    PENDING = "pending"
    PAID = "paid"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

# ============================= MODELS ================================
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