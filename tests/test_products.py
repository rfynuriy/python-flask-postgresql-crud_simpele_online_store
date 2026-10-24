

def test_view_products(client, dummy_product):
    response = client.get("/view/products")

    assert response.json[0]["product_name"] == "sikat_gigi"
    assert len(response.json) == 1
    assert response.status_code == 200

def test_view_products_without_product(client):
    response = client.get("/view/products")

    assert response.json == []
    assert len(response.json) == 0
    assert response.status_code == 200