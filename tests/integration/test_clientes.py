def test_listar_clientes_vacio(client, auth_headers):
    respuesta = client.get("/clientes", headers=auth_headers)

    assert respuesta.status_code == 200
    assert respuesta.get_json() == []


def test_crear_cliente_correcto(client, auth_headers):
    datos = {
        "nombre": "Adrian",
        "email": "adrian@gmail.com",
        "telefono": "600123456"
    }

    respuesta = client.post(
        "/clientes",
        json=datos,
        headers=auth_headers
    )

    assert respuesta.status_code == 201

    cliente = respuesta.get_json()

    assert cliente["nombre"] == "Adrian"
    assert cliente["email"] == "adrian@gmail.com"
    assert cliente["telefono"] == "600123456"
    assert "id" in cliente


def test_crear_cliente_email_invalido(client, auth_headers):
    datos = {
        "nombre": "Adrian",
        "email": "adriangmail.com",
        "telefono": "600123456"
    }

    respuesta = client.post(
        "/clientes",
        json=datos,
        headers=auth_headers
    )

    assert respuesta.status_code == 400


def test_crear_cliente_sin_telefono(client, auth_headers):
    datos = {
        "nombre": "Adrian",
        "email": "adrian@gmail.com"
    }

    respuesta = client.post(
        "/clientes",
        json=datos,
        headers=auth_headers
    )

    assert respuesta.status_code == 201
    assert respuesta.get_json()["telefono"] == ""


def test_obtener_cliente(client, auth_headers):
    datos = {
        "nombre": "Miguel",
        "email": "miguel@gmail.com",
        "telefono": "611111111"
    }

    creacion = client.post(
        "/clientes",
        json=datos,
        headers=auth_headers
    )

    id_cliente = creacion.get_json()["id"]

    respuesta = client.get(
        f"/clientes/{id_cliente}",
        headers=auth_headers
    )

    assert respuesta.status_code == 200
    assert respuesta.get_json()["nombre"] == "Miguel"


def test_obtener_cliente_inexistente(client, auth_headers):
    respuesta = client.get(
        "/clientes/9999",
        headers=auth_headers
    )

    assert respuesta.status_code == 404


def test_actualizar_cliente(client, auth_headers):
    datos = {
        "nombre": "Samuel",
        "email": "samuel@gmail.com",
        "telefono": "622222222"
    }

    creacion = client.post(
        "/clientes",
        json=datos,
        headers=auth_headers
    )

    id_cliente = creacion.get_json()["id"]

    nuevos_datos = {
        "nombre": "Samuel Nuevo",
        "email": "samuel.nuevo@gmail.com",
        "telefono": "633333333"
    }

    respuesta = client.put(
        f"/clientes/{id_cliente}",
        json=nuevos_datos,
        headers=auth_headers
    )

    assert respuesta.status_code == 200
    assert respuesta.get_json()["nombre"] == "Samuel Nuevo"
    assert respuesta.get_json()["email"] == "samuel.nuevo@gmail.com"
    assert respuesta.get_json()["telefono"] == "633333333"


def test_actualizar_cliente_inexistente(client, auth_headers):
    datos = {
        "nombre": "Adrian",
        "email": "adrian@gmail.com"
    }

    respuesta = client.put(
        "/clientes/9999",
        json=datos,
        headers=auth_headers
    )

    assert respuesta.status_code == 404


def test_actualizar_cliente_datos_invalidos(client, auth_headers):
    datos = {
        "nombre": "Adrian",
        "email": "adrian@gmail.com",
        "telefono": "600123456"
    }

    creacion = client.post(
        "/clientes",
        json=datos,
        headers=auth_headers
    )

    id_cliente = creacion.get_json()["id"]

    datos_invalidos = {
        "nombre": "Adrian",
        "email": "adriangmail.com",
        "telefono": "600123456"
    }

    respuesta = client.put(
        f"/clientes/{id_cliente}",
        json=datos_invalidos,
        headers=auth_headers
    )

    assert respuesta.status_code == 400


def test_eliminar_cliente(client, auth_headers):
    datos = {
        "nombre": "Adrian",
        "email": "adrian@gmail.com",
        "telefono": "600123456"
    }

    creacion = client.post(
        "/clientes",
        json=datos,
        headers=auth_headers
    )

    id_cliente = creacion.get_json()["id"]

    respuesta = client.delete(
        f"/clientes/{id_cliente}",
        headers=auth_headers
    )

    assert respuesta.status_code == 204

    comprobacion = client.get(
        f"/clientes/{id_cliente}",
        headers=auth_headers
    )

    assert comprobacion.status_code == 404


def test_eliminar_cliente_inexistente(client, auth_headers):
    respuesta = client.delete(
        "/clientes/9999",
        headers=auth_headers
    )

    assert respuesta.status_code == 404