import pytest

from app.extensions import db, bcrypt
from config import TestingConfig
from app import create_app
from app.models import Users, UserRole

app = create_app(TestingConfig)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    assert app.config["SQLALCHEMY_DATABASE_URI"].endswith("_test"), \
        "STOP: ini bukan database test!"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

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

