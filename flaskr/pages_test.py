from flaskr import create_app

import pytest

# See https://flask.palletsprojects.com/en/2.2.x/testing/
# for more info on testing
@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_home_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Welcome to RetroPedia! we're still working on the name" in resp.data


def test_page_index(client):
    resp = client.get("/pages")
    assert resp.status_code == 200


def test_about(client):
    resp = client.get("/about")
    assert resp.status_code == 200

    # check if author images are being displayed
    assert b"Cambrell" in resp.data
    assert b"Samuel" in resp.data
    assert b"Angel" in resp.data


def test_fetch_images(client):
    resp = client.get("/image/Cambrell.jpg")
    assert resp.status_code == 200


def test_page(client):
    resp = client.get("/pages/super-mario-bros-1985")
    assert resp.status_code == 200


def test_login(client):
    resp = client.post("/login", data={"username": "test_user", "password": "test_password"})
    assert resp.status_code == 302  # Redirect status code


def test_signup(client):
    resp = client.post("/signup", data={"username": "test_user", "password": "test_password"})
    assert resp.status_code == 302  # Redirect status code


def test_upload_file(client):
    # Ensure the user is authenticated to upload a file
    resp = client.post("/upload", data={"username": "test_user", "password": "test_password"})
    assert resp.status_code == 302  # Redirect status code
    assert b"Please log in" in resp.data

def test_about_page(client):
    client.post("/login", data={"username": "test_user", "password": "test_password"})
    resp = client.post("/upload", data={"username": "test_user", "password": "test_password"})
    assert resp.status_code == 302  # Redirect status code
