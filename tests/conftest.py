import pytest

from app.extensions import db, bcrypt
from config import TestingConfig
from app import create_app
from app.models import Users, UserRole, Products



@pytest.fixture
def app():
    app = create_app(TestingConfig)
    assert app.config["SQLALCHEMY_DATABASE_URI"].endswith("_test"), \
            "STOP: ini bukan database test!"
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def dummy_user_admin(app):
    password_hash = bcrypt.generate_password_hash("rahasia123").decode("utf-8")
    admin = Users(
        username= "rfynuriy",
        email= "admin_ganteng@gmail.com",
        password_hash= password_hash,
        phone_number= "081111111111",
        role= UserRole.ADMIN
    )
    db.session.add(admin)
    db.session.commit()
    return admin

@pytest.fixture
def dummy_user_customer(app):
    password_hash = bcrypt.generate_password_hash("rahasia123").decode("utf-8")
    customer = Users(
        username= "dummy_customer",
        email= "custommer@gmail.com",
        password_hash= password_hash,
        phone_number= "081111111112",
        role= UserRole.CUSTOMER
    )
    db.session.add(customer)
    db.session.commit()
    return customer

@pytest.fixture
def dummy_user_seller(app):
    password_hash = bcrypt.generate_password_hash("rahasia123").decode("utf-8")
    seller = Users(
        username= "dummy_seller",
        email= "alat_mandi@gmail.com",
        password_hash= password_hash,
        phone_number= "081111111113",
        role= UserRole.SELLER
    )
    db.session.add(seller)
    db.session.commit()
    return seller

@pytest.fixture
def dummy_product(dummy_user_seller):
    product = Products(
        seller_id= dummy_user_seller.id,
        product_name= "sikat_gigi",
        price= 7000,
        stok= 12,
        description= None
    )
    db.session.add(product)
    db.session.commit()
    return product

@pytest.fixture(name="auth_customer")
def auth_headers_customer(client, dummy_user_customer):
    pyload = {
        "username": dummy_user_customer.username,
        "password": "rahasia123"
    }
    response = client.post("/login", json=pyload)
    assert response.status_code == 200, "login failed"
    token = response.get_json().get("access_token")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    return headers

@pytest.fixture(name="auth_seller")
def auth_headers_seller(client, dummy_user_seller):
    pyload = {
        "username": dummy_user_seller.username,
        "password": "rahasia123"
    }
    response = client.post("/login", json=pyload)
    assert response.status_code == 200, "login failed"
    token = response.get_json().get("access_token")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    return headers