import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST

def create_database() -> None:
    """Создаёт новую базу данных PostgreSQL."""
    conn = psycopg2.connect(dbname="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
    cur.execute(f"CREATE DATABASE {DB_NAME}")
    cur.close()
    conn.close()

def create_tables() -> None:
    """Создаёт таблицы employers и vacancies в базе данных."""
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE employers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            url TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE vacancies (
            id SERIAL PRIMARY KEY,
            employer_id INTEGER REFERENCES employers(id),
            name TEXT NOT NULL,
            salary_from INTEGER,
            salary_to INTEGER,
            url TEXT
        )
    """)

    conn.commit()
    cur.close()
    conn.close()