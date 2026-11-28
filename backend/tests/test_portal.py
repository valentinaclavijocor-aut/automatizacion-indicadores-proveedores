"""Aislamiento entre proveedores y ocultamiento de borradores."""
API = "/api/v1"


def test_proveedor_ve_solo_sus_indicadores_publicados(client, prov_a_h, datos):
    r = client.get(f"{API}/mis-indicadores", headers=prov_a_h)
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1
    assert items[0]["periodo"] == "2026-09" and items[0]["valor"] == 95.5
    assert set(items[0]) == {"id", "periodo", "nombre", "valor", "unidad"}


def test_proveedor_no_ve_indicadores_de_otro_proveedor(client, prov_a_h, prov_b_h, datos):
    de_a = client.get(f"{API}/mis-indicadores", headers=prov_a_h).json()
    de_b = client.get(f"{API}/mis-indicadores", headers=prov_b_h).json()
    assert {i["id"] for i in de_a}.isdisjoint({i["id"] for i in de_b})
    assert de_b[0]["valor"] == 70.0


def test_proveedor_no_puede_forzar_otro_proveedor_por_parametro(client, prov_a_h, datos):
    # El proveedor_id enviado en la URL se ignora: el contrato dice que sale de la sesion.
    r = client.get(f"{API}/mis-indicadores?proveedor_id={datos['b'].id}", headers=prov_a_h)
    assert r.status_code == 200
    assert [i["valor"] for i in r.json()] == [95.5]


def test_borrador_no_aparece_en_el_portal(client, prov_a_h, datos):
    items = client.get(f"{API}/mis-indicadores?periodo=2026-10", headers=prov_a_h).json()
    assert items == []
    assert "2026-10" not in [p["periodo"] for p in client.get(f"{API}/mis-periodos", headers=prov_a_h).json()]


def test_al_publicar_el_indicador_pasa_a_ser_visible(client, admin_h, prov_a_h, datos):
    assert client.get(f"{API}/mis-indicadores?periodo=2026-10", headers=prov_a_h).json() == []
    client.post(f"{API}/publicaciones/{datos['pub_borrador'].id}/publicar", headers=admin_h)
    items = client.get(f"{API}/mis-indicadores?periodo=2026-10", headers=prov_a_h).json()
    assert len(items) == 1 and items[0]["nombre"] == "Calidad de productos"


def test_filtro_por_periodo_y_formato_invalido(client, prov_a_h):
    assert client.get(f"{API}/mis-indicadores?periodo=2026-09", headers=prov_a_h).status_code == 200
    assert client.get(f"{API}/mis-indicadores?periodo=2026-09", headers=prov_a_h).json() != []
    assert client.get(f"{API}/mis-indicadores?periodo=2030-01", headers=prov_a_h).json() == []
    assert client.get(f"{API}/mis-indicadores?periodo=malo", headers=prov_a_h).status_code == 422


def test_mis_periodos_solo_publicados_con_indicadores_propios(client, admin_h, prov_a_h, prov_b_h, datos):
    # B no tiene indicadores en 2026-10, A si; antes de publicar ninguno lo ve.
    client.post(f"{API}/publicaciones/{datos['pub_borrador'].id}/publicar", headers=admin_h)
    periodos_a = [p["periodo"] for p in client.get(f"{API}/mis-periodos", headers=prov_a_h).json()]
    periodos_b = [p["periodo"] for p in client.get(f"{API}/mis-periodos", headers=prov_b_h).json()]
    assert periodos_a == ["2026-10", "2026-09"]  # mas reciente primero
    assert periodos_b == ["2026-09"]


def test_usuario_desactivado_pierde_acceso_aunque_tenga_token(client, db_session, prov_a_h, datos):
    from app.models import Usuario

    db_session.query(Usuario).filter_by(correo="proveedor.a@demo.com").update({"activo": False})
    db_session.commit()
    assert client.get(f"{API}/mis-indicadores", headers=prov_a_h).status_code == 401
