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

def test_checkout_without_token(client, dummy_product):
    order = {
            "products_id": dummy_product.id,
            "quantity": 10
        }
    payload = {"items": [order]}
    response = client.post("/checkout", json=payload)

    assert response.status_code == 401
    assert response.json["msg"] == "Missing Authorization Header"
