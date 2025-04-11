from typing import List, Tuple, Any, Optional

import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST

class DBManager:
    """Класс для работы с базой данных PostgreSQL."""
    def __init__(self):
        self.conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

    def get_companies_and_vacancies_count(self) -> list[tuple[Any, ...]]:
        """Возвращает список компаний и количество их вакансий."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, COUNT(v.id)
                FROM employers e
                LEFT JOIN vacancies v ON e.id = v.employer_id
                GROUP BY e.name
            """)
            return cur.fetchall()

    def get_all_vacancies(self) -> list[tuple[Any, ...]]:
        """Возвращает список всех вакансий с деталями."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, v.name, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.id
            """)
            return cur.fetchall()

    def get_avg_salary(self) -> Optional[float]:
        """Возвращает среднюю зарплату по всем вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute("SELECT AVG(COALESCE(salary_from, salary_to)) FROM vacancies")
            return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> list[tuple[Any, ...]]:
        """Возвращает вакансии с зарплатой выше средней."""
        avg_salary = self.get_avg_salary()
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT name, salary_from, salary_to, url
                FROM vacancies
                WHERE COALESCE(salary_from, salary_to) > %s
            """, (avg_salary,))
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple[Any, ...]]:
        """Возвращает вакансии, содержащие ключевое слово в названии."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT name, salary_from, salary_to, url
                FROM vacancies
                WHERE name ILIKE %s
            """, (f"%{keyword}%",))
            return cur.fetchall()

    def close(self):
        self.conn.close()