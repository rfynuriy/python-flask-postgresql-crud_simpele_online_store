#test register
def test_regiter_user_succses(client):
    pyload = {
        "username": "rfynury",
        "email": "rafiemailgmail.com",
        "password_hash": "dj_almira_berto1",
        "phone_number": "089527358614",
    }
    response = client.post("/auth/register", json=pyload)

    assert response.status_code == 200
    assert response.json["message"] == "User JSON data successfully saved!"
    # or
    assert "User" in response.json["message"]


#login
def test_login_succses(client, dummy_user):
    pyload = {
        "username": dummy_user.username,
        "password": "rahasia123"
        }
    resposnse = client.post("/auth/login", json=pyload)

    assert resposnse.status_code == 200
    assert "access_token" in resposnse.json

def test_incorrect_login_password(client, dummy_user):
    pyload = {
        "username": dummy_user.username,
        "password": "pwsalah"
    }
    response = client.post("/auth/login", json=pyload)

    assert response.status_code == 401
    assert response.json["message"] == "Incorrect username or password"

def test_unregistered_login_username(client):
    pyload = {
        "username": "unregistered username!",
        "password": "rahasia123"
    }
    respose = client.post("/auth/login", json=pyload)

    assert respose.status_code == 401
    assert respose.json["message"] == "Incorrect username or password"
