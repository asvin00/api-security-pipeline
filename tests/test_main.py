import pytest

# Import the Flask app we created in app/main.py
from app.main import app


# @pytest.fixture creates a "client" that can make fake HTTP requests to our app
# We use "yield" instead of "return" so pytest can do cleanup after each test
@pytest.fixture
def client():
    # TESTING=True enables Flask's test mode (better error messages, no actual server needed)
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client   # each test function receives this "client" object


# TEST 1: Does the home page (/) return HTTP 200 (success)?
# "client" is automatically provided by the fixture above
def test_home_returns_200(client):
    response = client.get("/")         # simulate a GET request to /
    assert response.status_code == 200  # assert = "this MUST be true"

# TEST 2: Does the home page return the correct JSON data?
def test_home_message(client):
    response = client.get("/")
    data = response.get_json()           # parse the JSON response body
    assert data["status"] == "ok"     # check the "status" field
    assert "message" in data          # check the "message" field exists

# TEST 3: Does the /health endpoint return 200 and correct data?
def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"

# TEST 4: Does the /add endpoint correctly add two numbers?
def test_add_endpoint(client):
    response = client.get("/add/3/5")  # ask for 3 + 5
    data = response.get_json()
    assert data["result"] == 8         # answer must be 8

# TEST 5: What if we add negative numbers?
def test_add_negative_numbers(client):
    response = client.get("/add/-2/10")
    data = response.get_json()
    assert data["result"] == 8

# TEST 6: Does /add with 0 work?
def test_add_zero(client):
    response = client.get("/add/0/0")
    data = response.get_json()
    assert data["result"] == 0
