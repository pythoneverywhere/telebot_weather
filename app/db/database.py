import psycopg2

DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "tolik"
DB_PASSWORD = "123"
DB_NAME = "datatolik"
DB_TABLE = "users"


def setup_database():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {DB_TABLE} (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE NOT NULL
        )
        """)

        cursor.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"ошибка: {e}")


if __name__ == "__main__":
    setup_database()
