import pytest
from app import app, db, bcrypt, Users, UserRole


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLACHEMY_DATABASE_URI'] = 'sqlite///:memory:'

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
    db.session.commit
    return user

