import psycopg2


def conectar_db():

        conexion = psycopg2.connect(

        host="172.28.37.80",

        database="infralab",

        user="roman",

        password="1234"

        )

        return conexion
