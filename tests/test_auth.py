from app import bcrypt

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

def test_login_succses(client, dummy_user):
    pyload = {
        "username": dummy_user.username,
        "password": "rahasia123"
        }
    resposnse = client.post("/login", json=pyload)

    assert resposnse.status_code == 200
    assert "access_token" in resposnse.json