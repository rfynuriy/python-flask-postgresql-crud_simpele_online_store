import pytest
from app import CheckoutSchema

def test_CheckoutSchema():
    schema = CheckoutSchema()
    good_data = {
        "items": [
            {"products_id": 1, "quantity": 2}
        ]
    }
    errors = schema.validate(good_data)
    assert errors == {}

def test_CheckoutSchema_quantity_nol():
    schema = CheckoutSchema()
    Data_does_not_match = {
        "items": [
            {"products_id": 1, "quantity": 0}
        ]
    }
    errors = schema.validate(Data_does_not_match)
    assert "items" in errors

def test_CheckoutSchema_product_id_nol():
    schema = CheckoutSchema()
    Data_does_not_match = {
        "items": [
            {"products_id": 0, "quantity": 4}
        ]
    }
    errors = schema.validate(Data_does_not_match)
    assert errors != {}

@pytest.mark.parametrize("data_invalid",[
    {"items": [{"products_id": 0, "quantity": 1}]},
    {"items": [{"products_id": 1, "quantity": 0}]},
    {"items": [{"products_id": -1, "quantity": 1}]},
    {"items": [{"products_id": 1, "quantity": -1}]}
])

def test_combined_CheckoutSchema_error(data_invalid):
    schema  = CheckoutSchema()
    errors = schema.validate(data_invalid)
    assert errors != {}

def test_cek_fixture_client(client):
    response = client.get("/endpoint-palsu")
    assert response.status_code == 404
