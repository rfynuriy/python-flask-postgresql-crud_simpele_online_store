from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Numeric, ForeignKey

from decimal import Decimal

from app.extensions import db

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user import Users
    from .orders import ProductsOrders

# ============================== MODELS ===============================
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