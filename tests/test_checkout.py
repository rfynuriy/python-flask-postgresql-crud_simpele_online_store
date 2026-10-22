from app.extensions import db
from app.models import Orders
from sqlalchemy import select

def test_checkout_succses(client, auth_headers, dummy_product):
    order = {
        "products_id": dummy_product.id,
        "quantity": 10
    }
    pyload = {"items": [order]}
    response = client.post("/checkout", json=pyload, headers=auth_headers)

    assert response.status_code == 200
    assert response.json["message"] == "Checkout berhasil!"
    assert "order_id" in response.json

