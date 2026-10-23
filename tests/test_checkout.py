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

def test_checkout_quantity_nol(client, auth_headers, dummy_product):
    order = {
        "products_id": dummy_product.id,
        "quantity": 0
    }
    payload = {"items": [order]}
    response = client.post("/checkout", json=payload, headers=auth_headers)

    assert "items" in response.json
    assert response.status_code == 400

def test_checkout_products_not_found(client, auth_headers):
    order = {
        "products_id": 9999,
        "quantity": 3
    }
    payload = {"items": [order]}
    response = client.post("/checkout", json=payload, headers=auth_headers)

    assert "9999" in response.json["error"]
    assert response.status_code == 404

def test_checkout_exceeding_product(client, auth_headers, dummy_product):
    order = {
        "products_id": dummy_product.id,
        "quantity": 9999
    }
    payload = {"items": [order]}
    response = client.post("/checkout", json=payload, headers=auth_headers)

    assert "insufficient stock" in response.json["error"]
    assert response.status_code == 400
