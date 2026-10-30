import pytest
from app.schemas import CheckoutSchema, RegisterSchema, LoginSchema

# =================== test checkout schemas =================== #

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


# =================== test register schemas =================== #

def test_register_schema_success():
    schema = RegisterSchema()
    good_data = {
        "username": "rafinur",
        "email": "rafinury@gmail.com",
        "password_hash": "admin123",
        "phone_number": "089527358454"
    }
    errors = schema.validate(good_data)

    assert errors == {}

# === all required
@pytest.mark.parametrize("data, field",[
    ({
        "email": "rafinury@gmail.com",
        "password_hash": "admin123",
        "phone_number": "089527358454"
    }, "username"),
    ({
        "username": "rfynuriy",
        "password_hash": "admin123",
        "phone_number": "089527358454"
    },"email"),
    ({
        "username": "rfynuriy",
        "email": "rafinury@gmail.com",
        "phone_number": "089527358454"
    }, "password_hash"),
    ({
        "username": "rfynuriy",
        "email": "rafinury@gmail.com",
        "password_hash": "admin123"
    }, "phone_number")
]) # test required username, email, password , phone_number
def test_register_field(data, field):
    schema = RegisterSchema()
    errors = schema.validate(data)

    assert field in errors

# === bad username
@pytest.mark.parametrize("username_violates_the_rules", [
    {
        "username": "rh",
        "email": "rafinury@gmail.com",
        "password_hash": "admin123",
        "phone_number": "089527358454"
    },
    {
        "username": "a" * 31,
        "email": "rafinury@gmail.com",
        "password_hash": "admin123",
        "phone_number": "089527358454"
    }
])
def test_register_schema_username_failed(username_violates_the_rules):
    schema = RegisterSchema()
    errors = schema.validate(username_violates_the_rules)

    assert "username" in errors

# === bad email
@pytest.mark.parametrize("bad_email", [
    {
        "username": "rfynuriy",
        "email": "rafinury@gmail",
        "password_hash": "admin123",
        "phone_number": "089527358454"
    },
    {
        "username": "rfynuriy",
        "email": "rafinury@gmail.s",
        "password_hash": "admin123",
        "phone_number": "089527358454"
    },
    {
        "username": "rfynuriy",
        "email": "rafinurygmail.com",
        "password_hash": "admin123",
        "phone_number": "089527358454"
    }
])
def test_register_schema_email_failed(bad_email):
    schema = RegisterSchema()
    errors = schema.validate(bad_email)

    assert "email" in errors

# === bad password
@pytest.mark.parametrize("bad_password", [
    {
        "username": "rfynuriy",
        "email": "rafinury@gmail.com",
        "password_hash": "a" * 7,
        "phone_number": "08952735666"
    },
    {
        "username": "rfynuriy",
        "email": "rafinury@gmail.com",
        "password_hash": "a" * 73,
        "phone_number": "08952735666"
    }
])
def test_register_invalid_password(bad_password):
    schema = RegisterSchema()
    errors = schema.validate(bad_password)

    assert "password_hash" in errors

# === bad number
@pytest.mark.parametrize("bad_number", [
    {
        "username": "rfynuriy",
        "email": "rafinury@gmail.com",
        "password_hash": "admin123",
        "phone_number": "08952735halo"
    },
    {
        "username": "rfynuriy",
        "email": "rafinury@gmail.com",
        "password_hash": "admin123",
        "phone_number": "02345678"
    },
    {
        "username": "rfynuriy",
        "email": "rafinury@gmail.com",
        "password_hash": "admin123",
        "phone_number": "012345678910111111111"
    }
])
def test_register_schema_invalid_number(bad_number):
    schema = RegisterSchema()
    errors = schema.validate(bad_number)

    assert "phone_number" in errors


# =================== test login schemas =================== #

def test_login_schema():
    schema = LoginSchema()
    good_data = {
        "username": "rfynuriy",
        "password": "admin123"
    }
    errors = schema.validate(good_data)

    assert errors == {}

# === all required
@pytest.mark.parametrize("data, field", [
    ({"username": "rfynuriy"}, "password"),
    ({"password": "admin123"}, "username")
])

def test_login_field(data, field):
    schema = LoginSchema()
    errors = schema.validate(data)

    assert field in errors