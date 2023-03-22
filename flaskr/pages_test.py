import io
import os
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
    assert b"Welcome to team's SPONGEBOB's Project" in resp.data


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
    resp = client.get("/image/IMG_20210621_161958736_2.jpg")
    assert resp.status_code == 200


def test_page(client):
    resp = client.get("/pages/Super-Mario-Bros-1985")
    assert resp.status_code == 200


def test_signup(client):
    resp = client.post("/signup",
                       data={
                           "username": "test_user",
                           "password": "test_password"
                       })
    assert resp.status_code == 302  # Redirect status code


def test_login(client):
    resp = client.post("/login", data={"username": "sam", "password": "1234"})
    assert resp.status_code == 302  # Redirect status code


def test_upload_file(client):
    # Log in the user before uploading a file
    client.post("/login", data={"username": "sam", "password": "1234"})

    # Replace the file path with the correct path to your test image
    file_path = os.path.join(os.path.dirname(__file__), "test_image.jpg")

    # Use the file_path variable in the request
    with open(file_path, "rb") as f:
        resp = client.post("/upload", data={"file": f})

    assert resp.status_code == 302  # Redirect status code


def test_about_page(client):
    # Log in the user before accessing the about page
    client.post("/login", data={"username": "sam", "password": "1234"})
    resp = client.get("/about")
    assert resp.status_code == 200
