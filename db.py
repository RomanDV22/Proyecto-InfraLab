import os

from dotenv import load_dotenv
from psycopg2.pool import ThreadedConnectionPool

load_dotenv()

_pool = None


def _obtener_pool():
    global _pool

    if _pool is None:
        _pool = ThreadedConnectionPool(
            1, 10,
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

    return _pool


def conectar_db():
    return _obtener_pool().getconn()


def liberar_db(conexion):
    _obtener_pool().putconn(conexion)
