import pytest

from app.extensions import db, bcrypt
from config import TestingConfig
from app import create_app
from app.models import Users, UserRole



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
def dummy_user(client):
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

