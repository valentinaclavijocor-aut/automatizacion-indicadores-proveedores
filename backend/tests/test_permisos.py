"""Un PROVEEDOR no puede usar endpoints de ADMIN, y un ADMIN no usa el portal de proveedores."""
API = "/api/v1"

RUTAS_ADMIN_GET = ["/proveedores", "/proveedores/1", "/publicaciones", "/indicadores", "/notificaciones"]


def test_proveedor_no_puede_usar_endpoints_admin_403(client, prov_a_h, datos):
    for ruta in RUTAS_ADMIN_GET:
        assert client.get(f"{API}{ruta}", headers=prov_a_h).status_code == 403, ruta
    assert client.post(f"{API}/publicaciones", json={"periodo": "2026-11"}, headers=prov_a_h).status_code == 403
    assert client.post(f"{API}/publicaciones/{datos['pub_borrador'].id}/publicar", headers=prov_a_h).status_code == 403
    cuerpo = {"proveedor_id": datos["a"].id, "publicacion_id": datos["pub_borrador"].id,
              "nombre": "X", "valor": 1, "unidad": "%"}
    assert client.post(f"{API}/indicadores", json=cuerpo, headers=prov_a_h).status_code == 403
    assert client.post(f"{API}/notificaciones/1/enviar", headers=prov_a_h).status_code == 403


def test_admin_no_puede_usar_portal_proveedor_403(client, admin_h):
    assert client.get(f"{API}/mis-indicadores", headers=admin_h).status_code == 403
    assert client.get(f"{API}/mis-periodos", headers=admin_h).status_code == 403
