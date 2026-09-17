def test_listar_productos_vacio(client, auth_headers):
    respuesta = client.get("/productos", headers=auth_headers)

    assert respuesta.status_code == 200
    assert respuesta.get_json() == []


def test_crear_producto_correcto(client, auth_headers):
    datos = {
        "nombre": "Teclado",
        "precio": 19.99,
        "stock": 10
    }

    respuesta = client.post(
        "/productos",
        json=datos,
        headers=auth_headers
    )

    assert respuesta.status_code == 201

    producto = respuesta.get_json()

    assert producto["nombre"] == "Teclado"
    assert producto["precio"] == 19.99
    assert producto["stock"] == 10
    assert "id" in producto


def test_crear_producto_invalido(client, auth_headers):
    datos = {
        "nombre": "Teclado",
        "precio": -5,
        "stock": 10
    }

    respuesta = client.post(
        "/productos",
        json=datos,
        headers=auth_headers
    )

    assert respuesta.status_code == 400


def test_obtener_producto(client, auth_headers):
    datos = {
        "nombre": "Monitor",
        "precio": 150,
        "stock": 4
    }

    creacion = client.post(
        "/productos",
        json=datos,
        headers=auth_headers
    )

    id_producto = creacion.get_json()["id"]

    respuesta = client.get(
        f"/productos/{id_producto}",
        headers=auth_headers
    )

    assert respuesta.status_code == 200
    assert respuesta.get_json()["nombre"] == "Monitor"


def test_obtener_producto_inexistente(client, auth_headers):
    respuesta = client.get(
        "/productos/9999",
        headers=auth_headers
    )

    assert respuesta.status_code == 404


def test_actualizar_producto(client, auth_headers):
    datos = {
        "nombre": "Raton",
        "precio": 20,
        "stock": 5
    }

    creacion = client.post(
        "/productos",
        json=datos,
        headers=auth_headers
    )

    id_producto = creacion.get_json()["id"]

    nuevos_datos = {
        "nombre": "Raton Gaming",
        "precio": 35,
        "stock": 3
    }

    respuesta = client.put(
        f"/productos/{id_producto}",
        json=nuevos_datos,
        headers=auth_headers
    )

    assert respuesta.status_code == 200
    assert respuesta.get_json()["nombre"] == "Raton Gaming"
    assert respuesta.get_json()["precio"] == 35
    assert respuesta.get_json()["stock"] == 3


def test_actualizar_producto_inexistente(client, auth_headers):
    datos = {
        "nombre": "Teclado",
        "precio": 20,
        "stock": 5
    }

    respuesta = client.put(
        "/productos/9999",
        json=datos,
        headers=auth_headers
    )

    assert respuesta.status_code == 404


def test_actualizar_producto_datos_invalidos(client, auth_headers):
    datos = {
        "nombre": "Raton",
        "precio": 20,
        "stock": 5
    }

    creacion = client.post(
        "/productos",
        json=datos,
        headers=auth_headers
    )

    id_producto = creacion.get_json()["id"]

    datos = {
        "nombre": "Impresora",
        "precio": 200,
        "stock": 3.5
    }
    respuesta = client.put(
        f"/productos/{id_producto}",
        json=datos,
        headers=auth_headers
    )

    assert respuesta.status_code == 400


def test_eliminar_producto(client, auth_headers):
    datos = {
        "nombre": "Webcam",
        "precio": 40,
        "stock": 2
    }

    creacion = client.post(
        "/productos",
        json=datos,
        headers=auth_headers
    )

    id_producto = creacion.get_json()["id"]

    respuesta = client.delete(
        f"/productos/{id_producto}",
        headers=auth_headers
    )

    assert respuesta.status_code == 204

    comprobacion = client.get(
        f"/productos/{id_producto}",
        headers=auth_headers
    )

    assert comprobacion.status_code == 404


def test_eliminar_producto_inexistente(client, auth_headers):
    respuesta = client.delete(
        "/productos/9999",
        headers=auth_headers
    )

    assert respuesta.status_code == 404