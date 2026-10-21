from app.services import create_order
from app.models import Orders
from sqlalchemy import select
from app.extensions import db
from app.errors import InsufficientStockError, ProductNotFoundError
import pytest


def test_order_service(dummy_product, dummy_user):
    user_id = dummy_user.id
    pyload = [
        {
            "products_id": dummy_product.id,
            "quantity": 3
        }
    ]
    order = create_order(user_id, pyload)
    assert order.id is not None
    assert order.user_id == user_id
    db.session.refresh(dummy_product)
    assert dummy_product.stok == 9

def test_out_of_stok_order_service(dummy_product, dummy_user,):
    user_id = dummy_user.id
    pyload = [
        {
            "products_id": dummy_product.id,
            "quantity": 100
        }
    ]
    output_error = "I apologize, but there is insufficient stock."
    with pytest.raises(InsufficientStockError, match=output_error) :
        create_order(user_id, pyload)
    db.session.refresh(dummy_product)
    assert dummy_product.stok == 12
    all_orders= db.session.scalars(select(Orders)).all()
    assert len(all_orders) == 0

def test_product_not_found_order_service(dummy_product, dummy_user,):
    user_id = dummy_user.id
    pyload = [
        {
            "products_id": 100,
            "quantity": 1
        }
    ]
    output_error = "not found."
    with pytest.raises(ProductNotFoundError, match=output_error) :
        create_order(user_id, pyload)
    db.session.refresh(dummy_product)
    assert dummy_product.stok == 12
    all_orders= db.session.scalars(select(Orders)).all()
    assert len(all_orders) == 0
