import os

os.environ["DB_NAME"] = "infralab_test"

import db

db._pool = None

import pytest

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "database", "schema.sql")


@pytest.fixture(scope="session", autouse=True)
def _preparar_esquema():

    conexion = db.conectar_db()

    try:
        cursor = conexion.cursor()

        with open(SCHEMA_PATH) as archivo:
            cursor.execute(archivo.read())

        conexion.commit()
        cursor.close()

    finally:
        db.liberar_db(conexion)

    yield


@pytest.fixture(autouse=True)
def _limpiar_tablas():

    yield

    conexion = db.conectar_db()

    try:
        cursor = conexion.cursor()

        cursor.execute(
            "TRUNCATE metricas, alertas, clientes, requests RESTART IDENTITY CASCADE"
        )

        conexion.commit()
        cursor.close()

    finally:
        db.liberar_db(conexion)
