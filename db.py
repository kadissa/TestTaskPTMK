from dotenv import load_dotenv

from core import connect_db

load_dotenv()


def create_table():
    """Создаёт таблицу сотрудников, если её нет."""
    with connect_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            birth_date DATE NOT NULL,
            gender VARCHAR(10) CHECK (gender IN ('Male', 'Female'))
        );""")
        conn.commit()


def create_indexes():
    """Создаёт индексы для оптимизации запросов."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_fullname_sorted "
            "ON employees (full_name ) WHERE full_name LIKE 'F%';")
        conn.commit()


if __name__ == "__main__":
    create_table()
    print("Table has been created.")
    create_indexes()
    print("Index has been created.")

