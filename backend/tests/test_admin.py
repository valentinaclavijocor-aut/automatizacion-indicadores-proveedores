API = "/api/v1"


def test_admin_lista_y_obtiene_proveedores(client, admin_h, datos):
    r = client.get(f"{API}/proveedores", headers=admin_h)
    assert r.status_code == 200 and len(r.json()) == 2
    assert set(r.json()[0]) == {"id", "nit", "nombre", "correo", "activo"}
    assert client.get(f"{API}/proveedores/{datos['a'].id}", headers=admin_h).status_code == 200
    assert client.get(f"{API}/proveedores/9999", headers=admin_h).status_code == 404


def test_admin_crea_publicacion_y_duplicado_409(client, admin_h):
    r = client.post(f"{API}/publicaciones", json={"periodo": "2026-11"}, headers=admin_h)
    assert r.status_code == 201
    assert r.json()["estado"] == "BORRADOR" and r.json()["fecha_publicacion"] is None
    assert client.post(f"{API}/publicaciones", json={"periodo": "2026-11"}, headers=admin_h).status_code == 409


def test_periodo_con_formato_invalido_422(client, admin_h):
    for malo in ("2026-13", "202611", "26-11", "2026-1", ""):
        assert client.post(f"{API}/publicaciones", json={"periodo": malo}, headers=admin_h).status_code == 422, malo


def test_admin_registra_indicador(client, admin_h, datos):
    cuerpo = {"proveedor_id": datos["b"].id, "publicacion_id": datos["pub_borrador"].id,
              "nombre": "Calidad de productos", "valor": 98.0, "unidad": "%"}
    r = client.post(f"{API}/indicadores", json=cuerpo, headers=admin_h)
    assert r.status_code == 201
    assert r.json()["valor"] == 98.0 and r.json()["proveedor_id"] == datos["b"].id


def test_indicador_reglas_de_validacion(client, admin_h, datos):
    base = {"proveedor_id": datos["a"].id, "publicacion_id": datos["pub_borrador"].id,
            "nombre": "X", "valor": 1, "unidad": "%"}
    assert client.post(f"{API}/indicadores", json={**base, "proveedor_id": 999}, headers=admin_h).status_code == 404
    assert client.post(f"{API}/indicadores", json={**base, "publicacion_id": 999}, headers=admin_h).status_code == 404
    # Publicacion ya PUBLICADA: no se agregan indicadores.
    assert client.post(f"{API}/indicadores", json={**base, "publicacion_id": datos["pub_ok"].id},
                       headers=admin_h).status_code == 409
    for malo in ({**base, "valor": "abc"}, {**base, "nombre": ""}, {**base, "unidad": ""}, {k: v for k, v in base.items() if k != "valor"}):
        assert client.post(f"{API}/indicadores", json=malo, headers=admin_h).status_code == 422


def test_admin_filtra_indicadores(client, admin_h, datos):
    todos = client.get(f"{API}/indicadores", headers=admin_h).json()
    assert len(todos) == 3
    de_b = client.get(f"{API}/indicadores?proveedor_id={datos['b'].id}", headers=admin_h).json()
    assert len(de_b) == 1 and de_b[0]["proveedor_id"] == datos["b"].id
    combinado = client.get(
        f"{API}/indicadores?proveedor_id={datos['a'].id}&publicacion_id={datos['pub_borrador'].id}", headers=admin_h
    ).json()
    assert len(combinado) == 1


def test_publicar_cambia_estado_y_genera_notificaciones_pendientes(client, admin_h, datos):
    pub_id = datos["pub_borrador"].id  # solo tiene indicadores del proveedor A
    r = client.post(f"{API}/publicaciones/{pub_id}/publicar", headers=admin_h)
    assert r.status_code == 200
    assert r.json()["estado"] == "PUBLICADO"
    assert r.json()["fecha_publicacion"].endswith("Z")

    notifs = client.get(f"{API}/notificaciones", headers=admin_h).json()
    assert len(notifs) == 1
    assert notifs[0]["estado"] == "PENDIENTE" and notifs[0]["proveedor_id"] == datos["a"].id
    assert notifs[0]["correo_destino"] == "contacto.a@demo.com" and notifs[0]["fecha_envio"] is None


def test_publicar_dos_veces_409_y_inexistente_404(client, admin_h, datos):
    pub_id = datos["pub_borrador"].id
    assert client.post(f"{API}/publicaciones/{pub_id}/publicar", headers=admin_h).status_code == 200
    assert client.post(f"{API}/publicaciones/{pub_id}/publicar", headers=admin_h).status_code == 409
    assert client.post(f"{API}/publicaciones/9999/publicar", headers=admin_h).status_code == 404


def test_publicar_sin_indicadores_409(client, admin_h):
    pub = client.post(f"{API}/publicaciones", json={"periodo": "2027-01"}, headers=admin_h).json()
    r = client.post(f"{API}/publicaciones/{pub['id']}/publicar", headers=admin_h)
    assert r.status_code == 409


def test_enviar_notificacion_pendiente_de_implementar_501(client, admin_h, datos):
    client.post(f"{API}/publicaciones/{datos['pub_borrador'].id}/publicar", headers=admin_h)
    nid = client.get(f"{API}/notificaciones", headers=admin_h).json()[0]["id"]
    assert client.post(f"{API}/notificaciones/{nid}/enviar", headers=admin_h).status_code == 501
    assert client.post(f"{API}/notificaciones/9999/enviar", headers=admin_h).status_code == 404
