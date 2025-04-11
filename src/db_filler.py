from typing import List, Dict, Any

import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST

def insert_employers(employers: List[Dict[str, Any]]) -> None:
    """Добавляет работодателей в таблицу employers."""
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    cur = conn.cursor()
    for emp in employers:
        cur.execute(
            "INSERT INTO employers (id, name, url) VALUES (%s, %s, %s) ON CONFLICT (id) DO NOTHING",
            (int(emp['id']), emp['name'], emp['alternate_url'])
        )
    conn.commit()
    cur.close()
    conn.close()

def insert_vacancies(employer_id: int, vacancies: List[Dict[str, Any]]) -> None:
    """Добавляет вакансии работодателя в таблицу vacancies."""
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    cur = conn.cursor()
    for vac in vacancies:
        salary = vac.get('salary')
        salary_from = salary['from'] if salary and salary.get('from') else None
        salary_to = salary['to'] if salary and salary.get('to') else None
        cur.execute(
            """
            INSERT INTO vacancies (employer_id, name, salary_from, salary_to, url)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (employer_id, vac['name'], salary_from, salary_to, vac['alternate_url'])
        )
    conn.commit()
    cur.close()
    conn.close()