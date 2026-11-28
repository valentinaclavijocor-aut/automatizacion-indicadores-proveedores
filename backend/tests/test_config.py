from app.core.config import Settings


def test_url_postgresql_se_normaliza_a_psycopg2():
    s = Settings(database_url="postgresql://u:p@localhost:5432/db", secret_key="x")
    assert s.database_url.startswith("postgresql+psycopg2://")


def test_url_con_driver_explicito_no_cambia():
    s = Settings(database_url="sqlite://", secret_key="x")
    assert s.database_url == "sqlite://"
