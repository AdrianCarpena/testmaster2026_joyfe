import pytest

from app import crear_app


@pytest.fixture
def app(tmp_path):
    ruta_db = tmp_path / "tests.db"

    app = crear_app(str(ruta_db))
    app.config.update({
        "TESTING": True
    })

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def usuario(client):
    datos = {
        "username": "usuario_test",
        "password": "1234"
    }

    respuesta = client.post("/registro", json=datos)

    assert respuesta.status_code == 201

    return datos


@pytest.fixture
def token(client, usuario):
    respuesta = client.post("/login", json=usuario)

    assert respuesta.status_code == 200

    return respuesta.get_json()["token"]


@pytest.fixture
def auth_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }