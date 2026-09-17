from app import validar_registro, validar_producto, validar_cliente


# ---------------- REGISTRO ----------------

def test_registro_correcto():
    datos = {
        "username": "adrian",
        "password": "1234"
    }

    assert validar_registro(datos) is None


def test_registro_cuerpo_invalido():
    assert validar_registro("datos incorrectos") == "Cuerpo de la peticion invalido"


def test_registro_sin_username():
    datos = {
        "password": "1234"
    }

    assert validar_registro(datos) == "El campo username es obligatorio"


def test_registro_password_corta():
    datos = {
        "username": "adrian",
        "password": "123"
    }

    assert validar_registro(datos) == "El campo password debe tener al menos 4 caracteres"


# ---------------- PRODUCTO ----------------

def test_producto_correcto():
    datos = {
        "nombre": "Teclado",
        "precio": 19.99,
        "stock": 10
    }

    assert validar_producto(datos) is None


def test_producto_cuerpo_invalido():
    assert validar_producto("datos incorrectos") == "Cuerpo de la peticion invalido"


def test_producto_sin_nombre():
    datos = {
        "precio": 19.99,
        "stock": 10
    }

    assert validar_producto(datos) == "El campo nombre es obligatorio"


def test_producto_precio_invalido():
    datos = {
        "nombre": "Teclado",
        "precio": -1,
        "stock": 10
    }

    assert validar_producto(datos) == "El campo precio debe ser un numero >= 0"


def test_producto_stock_invalido():
    datos = {
        "nombre": "Teclado",
        "precio": 19.99,
        "stock": -1
    }

    assert validar_producto(datos) == "El campo stock debe ser un entero >= 0"

def test_producto_stock_decimal():
    datos = {
        "nombre": "Pantalla",
        "precio": 29.99,
        "stock": 2.5
    }

    assert validar_producto(datos) == "El campo stock debe ser un entero >= 0"

def test_producto_precio_str():
    datos = {
        "nombre": "Pantalla",
        "precio": "23",
        "stock": 2
    }

    assert validar_producto(datos) == "El campo precio debe ser un numero >= 0"

# ---------------- CLIENTE ----------------

def test_cliente_correcto():
    datos = {
        "nombre": "Adrian",
        "email": "adrian@gmail.com",
        "telefono": "600123123"
    }

    assert validar_cliente(datos) is None


def test_cliente_cuerpo_invalido():
    assert validar_cliente("datos incorrectos") == "Cuerpo de la peticion invalido"


def test_cliente_sin_nombre():
    datos = {
        "email": "adrian@gmail.com"
    }

    assert validar_cliente(datos) == "El campo nombre es obligatorio"


def test_cliente_email_invalido():
    datos = {
        "nombre": "Adrian",
        "email": "adriangmail.com"
    }

    assert validar_cliente(datos) == "El campo email no es valido"