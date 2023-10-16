# Python Imports
from fastapi.testclient import TestClient

# Custom imports
from innovationmerge.app import create_app
from app.sample import sample_division

# Creat Testing Client
app = create_app()
client = TestClient(app)


# Make sure to start function name with test
def test_sample_division():
    assert sample_division(1, 1) == 1


def test_user_token():
    # To check access_token functionality
    response = client.post(
        "/authenticate",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": "user1", "password": "user1@123"},
    )
    assert response.status_code == 200
    auth_token = response.json().get("access_token")
    assert len(auth_token) > 25

    # To check Incorrect username or password functionality
    response = client.post(
        "/authenticate",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": "user2@domain.com", "password": "user1@123"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


def test_user_me():
    # To check Not authenticated functionality
    response = client.get("/users/me/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

    # To get access_token
    response = client.post(
        "/authenticate",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": "user1", "password": "user1@123"},
    )
    assert response.status_code == 200
    auth_token = "Bearer " + response.json().get("access_token")

    # To check user information functionality
    response = client.get(
        "/users/me/",
        headers={"Authorization": auth_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user1@example.com"


def test_test_api():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Status": "Working"}


def test_sample_api():
    response = client.post(
        "/authenticate",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": "user1", "password": "user1@123"},
    )
    assert response.status_code == 200
    auth_token = "Bearer " + response.json().get("access_token")

    response = client.post(
        "/v1/sample_api",
        headers={
            "Content-Type": "application/json",
            "Authorization": auth_token,
        },
        json={"val1": 2, "val2": 2},
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": "Success",
        "status_code": 200,
        "message": "No Exception",
        "data": 1,
    }

    response = client.post(
        "/v1/sample_api",
        headers={
            "Content-Type": "application/json",
            "Authorization": auth_token,
        },
        json={"val1": 0, "val2": 0},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Cannot divide by Zero"}
