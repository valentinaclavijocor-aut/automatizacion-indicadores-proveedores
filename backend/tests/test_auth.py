from tests.conftest import PASSWORD_PRUEBA

API = "/api/v1"


def test_login_valido_devuelve_token_y_usuario(client, datos):
    r = client.post(f"{API}/auth/login", json={"correo": "proveedor.a@demo.com", "password": PASSWORD_PRUEBA})
    assert r.status_code == 200
    cuerpo = r.json()
    assert cuerpo["token_type"] == "bearer" and cuerpo["access_token"]
    assert cuerpo["usuario"]["rol"] == "PROVEEDOR"
    assert cuerpo["usuario"]["proveedor_id"] == datos["a"].id
    assert "password_hash" not in cuerpo["usuario"]


def test_login_clave_incorrecta_401(client, datos):
    r = client.post(f"{API}/auth/login", json={"correo": "admin@demo.com", "password": "incorrecta"})
    assert r.status_code == 401


def test_login_correo_inexistente_401(client, datos):
    r = client.post(f"{API}/auth/login", json={"correo": "nadie@demo.com", "password": PASSWORD_PRUEBA})
    assert r.status_code == 401


def test_login_usuario_inactivo_401(client, datos):
    r = client.post(f"{API}/auth/login", json={"correo": "inactivo@demo.com", "password": PASSWORD_PRUEBA})
    assert r.status_code == 401


def test_me_devuelve_usuario_autenticado(client, prov_a_h):
    r = client.get(f"{API}/auth/me", headers=prov_a_h)
    assert r.status_code == 200
    assert r.json()["correo"] == "proveedor.a@demo.com"


def test_endpoints_protegidos_sin_token_401(client, datos):
    for ruta in ("/auth/me", "/proveedores", "/publicaciones", "/indicadores",
                 "/mis-indicadores", "/mis-periodos", "/notificaciones"):
        assert client.get(f"{API}{ruta}").status_code == 401, ruta


def test_token_invalido_401(client, datos):
    r = client.get(f"{API}/auth/me", headers={"Authorization": "Bearer token.falso.xyz"})
    assert r.status_code == 401


def test_documentacion_swagger_disponible(client):
    assert client.get("/docs").status_code == 200
    assert client.get("/openapi.json").status_code == 200
