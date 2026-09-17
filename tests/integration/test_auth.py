def test_registro_correcto(client):
    datos = {
        "username": "adrian",
        "password": "1234"
    }

    respuesta = client.post("/registro", json=datos)

    assert respuesta.status_code == 201


def test_registro_sin_username(client):
    datos = {
        "password": "1234"
    }

    respuesta = client.post("/registro", json=datos)

    assert respuesta.status_code == 400


def test_registro_usuario_repetido(client):
    datos = {
        "username": "adrian",
        "password": "1234"
    }

    client.post("/registro", json=datos)
    respuesta = client.post("/registro", json=datos)

    assert respuesta.status_code == 409


def test_registro_password_vacia(client):
    datos = {
        "username": "adrian",
        "password": ""
    }

    respuesta = client.post("/registro", json=datos)

    assert respuesta.status_code == 400



def test_login_correcto(client, usuario):
    respuesta = client.post("/login", json=usuario)

    assert respuesta.status_code == 200
    assert "token" in respuesta.get_json()


def test_login_password_incorrecta(client, usuario):
    datos = {
        "username": usuario["username"],
        "password": "incorrecta"
    }

    respuesta = client.post("/login", json=datos)

    assert respuesta.status_code == 401


def test_login_usuario_inexistente(client):
    datos = {
        "username": "no_existe",
        "password": "1234"
    }

    respuesta = client.post("/login", json=datos)

    assert respuesta.status_code == 401


def test_login_username_vacio(client):
    datos = {
        "username": "",
        "password": "1234"
    }

    respuesta = client.post("/login", json=datos)

    assert respuesta.status_code == 401


def test_ruta_protegida_sin_token(client):
    respuesta = client.get("/productos")

    assert respuesta.status_code == 401


def test_ruta_protegida_token_invalido(client):
    headers = {
        "Authorization": "Bearer token_inventado"
    }

    respuesta = client.get("/productos", headers=headers)

    assert respuesta.status_code == 401


def test_ruta_protegida_token_correcto(client, auth_headers):
    respuesta = client.get("/productos", headers=auth_headers)

    assert respuesta.status_code == 200