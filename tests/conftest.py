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
def dummy_user(app):
    password_hash = bcrypt.generate_password_hash("rahasia123").decode("utf-8")
    user = Users(
        username= "rfynuriy",
        email= "hairafi@gmail.com",
        password_hash= password_hash,
        phone_number= "089527358614",
        role= UserRole.ADMIN
    )
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def dummy_seller(app):
    password_hash = bcrypt.generate_password_hash("rahasia123").decode("utf-8")
    seller = Users(
        username= "seller_mandi",
        email= "alat_mandi@gmail.com",
        password_hash= password_hash,
        phone_number= "089527358618",
        role= UserRole.SELLER
    )
    db.session.add(seller)
    db.session.commit()
    return seller

@pytest.fixture
def dummy_product(dummy_seller):
    product_1 = Products(
        seller_id= dummy_seller.id,
        product_name= "sikat_gigi",
        price= 7000,
        stok= 12,
        description= None
    )
    db.session.add(product_1)
    db.session.commit()
    return product_1
