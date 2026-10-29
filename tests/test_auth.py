# =================== /register =================== #
def test_regiter_user_succses(client):
    pyload = {
        "username": "rfynury",
        "email": "rafiemail@gmail.com",
        "password_hash": "dj_almira_berto1",
        "phone_number": "089527358614",
    }
    response = client.post("/register", json=pyload)

    assert response.status_code == 200
    assert response.json["message"] == "User JSON data successfully saved!"
    # or
    assert "User" in response.json["message"]

def test_register_duplicate_username(client, dummy_user_customer):
    pyload = {
        "username": dummy_user_customer.username,
        "email": "userganteng@gmail.com",
        "password_hash": "dj_kereta",
        "phone_number": "089187358619",
    }
    response = client.post("/register", json=pyload)
    assert response.status_code == 409
    assert "message" in response.json

def test_register_invalid_email(client):
    pyload = {
        "username": "rfyinfalid",
        "email": "infalidgmail.com",
        "password_hash": "admin123",
        "phone_number": "080877358614",
    }
    response = client.post("/register", json=pyload)

    assert response.status_code == 400
    assert "email" in response.json

def test_register_no_data(client):
    response = client.post("/register")

    assert response.status_code == 415
    assert response.json is None

def test_register_empty_data(client):
    pyload = {}
    response = client.post("/register", json=pyload)

    assert response.status_code == 400
    assert "username" in response.json
    assert "email" in response.json
    assert "password_hash" in response.json
    assert "phone_number" in response.json


# =================== /login =================== 
def test_login_succses(client, dummy_user_customer):
    pyload = {
        "username": dummy_user_customer.username,
        "password": "rahasia123"
        }
    resposnse = client.post("/login", json=pyload)

    assert resposnse.status_code == 200
    assert "access_token" in resposnse.json

def test_incorrect_login_password(client, dummy_user_customer):
    pyload = {
        "username": dummy_user_customer.username,
        "password": "pwsalah"
    }
    response = client.post("/login", json=pyload)

    assert response.status_code == 401
    assert response.json["message"] == "Incorrect username or password"

def test_unregistered_login_username(client):
    pyload = {
        "username": "unregistered username!",
        "password": "rahasia123"
    }
    respose = client.post("/login", json=pyload)

    assert respose.status_code == 401
    assert respose.json["message"] == "Incorrect username or password"
