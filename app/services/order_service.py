from app.extensions import db
from app.models import Products, ProductsOrders, Orders
from app.errors import InsufficientStockError, ProductNotFoundError


def create_order(user_id, items):
    try:
        new_order = Orders(user_id= user_id)
        db.session.add(new_order)

        db.session.flush()

        for item in items:
            products_id = item["products_id"]
            quantity = item["quantity"]

            product = db.session.get(Products, products_id)
            if not product:
                raise ProductNotFoundError(f"Product with ID {products_id} was not found.")
            if product.stok < quantity:
                raise InsufficientStockError("I apologize, but there is insufficient stock.")

            product.stok = product.stok-quantity

            detail_order = ProductsOrders(
                orders_id= new_order.id,
                products_id= product.id,
                purchase_quantity= quantity,
                purchase_price= product.price
            )
            db.session.add(detail_order)
        db.session.commit()
        return new_order

    except Exception:
        db.session.rollback()
        raise

