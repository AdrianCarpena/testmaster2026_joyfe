import sqlite3


# --------------------
# PRODUCTOS
# --------------------

def test_producto_se_guarda_en_bd(app, client, auth_headers):
    datos = {
        "nombre": "Teclado",
        "precio": 25,
        "stock": 10
    }

    respuesta = client.post(
        "/productos",
        json=datos,
        headers=auth_headers
    )

    id_producto = respuesta.get_json()["id"]

    conexion = sqlite3.connect(app.config["DATABASE"])

    producto = conexion.execute(
        "SELECT nombre, precio, stock FROM productos WHERE id = ?",
        (id_producto,)
    ).fetchone()

    conexion.close()

    assert producto is not None
    assert producto[0] == "Teclado"
    assert producto[1] == 25
    assert producto[2] == 10


def test_producto_invalido_no_se_guarda_en_bd(app, client, auth_headers):
    datos = {
        "nombre": "Monitor",
        "precio": -50,
        "stock": 5
    }

    client.post(
        "/productos",
        json=datos,
        headers=auth_headers
    )

    conexion = sqlite3.connect(app.config["DATABASE"])

    producto = conexion.execute(
        "SELECT * FROM productos WHERE nombre = ?",
        ("Monitor",)
    ).fetchone()

    conexion.close()

    assert producto is None


def test_actualizacion_producto_persiste(app, client, auth_headers):
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

    client.put(
        f"/productos/{id_producto}",
        json=nuevos_datos,
        headers=auth_headers
    )

    conexion = sqlite3.connect(app.config["DATABASE"])

    producto = conexion.execute(
        "SELECT nombre, precio, stock FROM productos WHERE id = ?",
        (id_producto,)
    ).fetchone()

    conexion.close()

    assert producto is not None
    assert producto[0] == "Raton Gaming"
    assert producto[1] == 35
    assert producto[2] == 3


def test_eliminacion_producto_persiste(app, client, auth_headers):
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

    client.delete(
        f"/productos/{id_producto}",
        headers=auth_headers
    )

    conexion = sqlite3.connect(app.config["DATABASE"])

    producto = conexion.execute(
        "SELECT * FROM productos WHERE id = ?",
        (id_producto,)
    ).fetchone()

    conexion.close()

    assert producto is None


# --------------------
# CLIENTES
# --------------------

def test_cliente_se_guarda_en_bd(app, client, auth_headers):
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

    id_cliente = respuesta.get_json()["id"]

    conexion = sqlite3.connect(app.config["DATABASE"])

    cliente = conexion.execute(
        "SELECT nombre, email, telefono FROM clientes WHERE id = ?",
        (id_cliente,)
    ).fetchone()

    conexion.close()

    assert cliente is not None
    assert cliente[0] == "Adrian"
    assert cliente[1] == "adrian@gmail.com"
    assert cliente[2] == "600123456"


def test_cliente_invalido_no_se_guarda_en_bd(app, client, auth_headers):
    datos = {
        "nombre": "Miguel",
        "email": "correo_incorrecto",
        "telefono": "611111111"
    }

    client.post(
        "/clientes",
        json=datos,
        headers=auth_headers
    )

    conexion = sqlite3.connect(app.config["DATABASE"])

    cliente = conexion.execute(
        "SELECT * FROM clientes WHERE nombre = ?",
        ("Miguel",)
    ).fetchone()

    conexion.close()

    assert cliente is None


def test_actualizacion_cliente_persiste(app, client, auth_headers):
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

    client.put(
        f"/clientes/{id_cliente}",
        json=nuevos_datos,
        headers=auth_headers
    )

    conexion = sqlite3.connect(app.config["DATABASE"])

    cliente = conexion.execute(
        "SELECT nombre, email, telefono FROM clientes WHERE id = ?",
        (id_cliente,)
    ).fetchone()

    conexion.close()

    assert cliente is not None
    assert cliente[0] == "Samuel Nuevo"
    assert cliente[1] == "samuel.nuevo@gmail.com"
    assert cliente[2] == "633333333"


def test_eliminacion_cliente_persiste(app, client, auth_headers):
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

    client.delete(
        f"/clientes/{id_cliente}",
        headers=auth_headers
    )

    conexion = sqlite3.connect(app.config["DATABASE"])

    cliente = conexion.execute(
        "SELECT * FROM clientes WHERE id = ?",
        (id_cliente,)
    ).fetchone()

    conexion.close()

    assert cliente is None


# --------------------
# USUARIOS Y TOKENS
# --------------------

def test_usuario_registrado_se_guarda_en_bd(app, client):
    datos = {
        "username": "adrian",
        "password": "1234"
    }

    client.post(
        "/registro",
        json=datos
    )

    conexion = sqlite3.connect(app.config["DATABASE"])

    usuario = conexion.execute(
        "SELECT username, password_hash FROM usuarios WHERE username = ?",
        ("adrian",)
    ).fetchone()

    conexion.close()

    assert usuario is not None
    assert usuario[0] == "adrian"
    assert usuario[1] != "1234"


def test_usuario_invalido_no_se_guarda_en_bd(app, client):
    datos = {
        "username": "adrian",
        "password": "12"
    }

    client.post(
        "/registro",
        json=datos
    )

    conexion = sqlite3.connect(app.config["DATABASE"])

    usuario = conexion.execute(
        "SELECT * FROM usuarios WHERE username = ?",
        ("adrian",)
    ).fetchone()

    conexion.close()

    assert usuario is None


def test_token_login_se_guarda_en_bd(app, client, usuario):
    respuesta = client.post(
        "/login",
        json=usuario
    )

    token = respuesta.get_json()["token"]

    conexion = sqlite3.connect(app.config["DATABASE"])

    token_bd = conexion.execute(
        "SELECT token, username FROM tokens WHERE token = ?",
        (token,)
    ).fetchone()

    conexion.close()

    assert token_bd is not None
    assert token_bd[0] == token
    assert token_bd[1] == usuario["username"]