from app import generar_token


def test_generar_token_devuelve_string():
    token = generar_token()

    assert isinstance(token, str)


def test_generar_token_longitud_correcta():
    token = generar_token()

    assert len(token) == 32


def test_generar_tokens_diferentes():
    token1 = generar_token()
    token2 = generar_token()

    assert token1 != token2


def test_generar_token_es_hexadecimal():
    token = generar_token()

    int(token, 16)