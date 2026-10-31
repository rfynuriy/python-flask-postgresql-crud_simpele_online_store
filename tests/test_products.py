# =================== /view/product =================== #

def test_view_products(client, dummy_product):
    response = client.get("/view/products")

    assert response.json[0]["product_name"] == "sikat_gigi"
    assert len(response.json) == 1
    assert response.status_code == 200

def test_view_products_without_product(client):
    response = client.get("/view/products")

    assert response.json == []
    assert response.status_code == 200

# =================== /add/products =================== #

def test_add_product_success(client, auth_seller):
    pyload = {
        "product_name": "sabun",
        "price": 5000,
        "stok": 40,
        "description": "capable of killing 99 percent of germs"
    }
    response = client.post("/add/product", json=pyload, headers=auth_seller)

    assert "Product successfully added" in response.json["message"]
    assert response.json["product_name"] == "sabun"
    assert response.status_code == 200

def test_add_product_without_seller(client, auth_customer):
    pyload = {
        "product_name": "lulur",
        "price": 200000,
        "stok": 98,
        "description": "capable of brightening the skin"
    }
    response = client.post("/add/product", json=pyload, headers=auth_customer)

    assert response.json["message"] == "You are not a seller"
    assert response.status_code == 403

def test_add_product_without_auth(client, dummy_product):
    pyload = {
        "product_name": "shampoo",
        "price": 15000,
        "stok": 20,
        "description": "capable of moisturizing hair"
    }
    response = client.post("/add/product", json=pyload)

    assert response.json["msg"] == "Missing Authorization Header"
    assert response.status_code == 401

def test_add_product_decimal_price(client, auth_seller):
    pyload = {
        "product_name": "sabun",
        "price": "19.99",
        "stok": 40,
        "description": "capable of killing 99 percent of germs"
    }
    response = client.post("/add/product", json=pyload, headers=auth_seller)

    assert response.status_code == 200
    assert type(response.json["price"]) == str

    results = client.get("/view/products")
    assert type(results.json[0]["price"]) == str
    assert results.json[0]["price"] == "19.99"