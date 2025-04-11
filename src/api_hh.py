from abc import ABC, abstractmethod
from typing import List, Optional
import requests
from config import BASE_URL

class JobAPI(ABC):
    """Абстрактный класс для работы с API вакансий."""

    @abstractmethod
    def get_vacancies(self, query: str, count: int) -> List[dict]:
        pass

    @abstractmethod
    def _connect_to_api(self, params: dict) -> Optional[dict]:
        pass

class HeadHunterAPI(JobAPI):
    """Класс для работы с API hh.ru."""

    def __init__(self):
        self.url = BASE_URL
        if not self.url:
            raise ValueError("BASE_URL is not set in environment variables.")

    def _connect_to_api(self, params: dict) -> Optional[dict]:
        """Выполняет запрос к API hh.ru и возвращает ответ."""
        try:
            response = requests.get(self.url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP ошибка: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при обращении к API: {e}")
        return None

    def get_vacancies(self, query: str, count: int = 10) -> List[dict]:
        """Возвращает список вакансий по запросу."""
        params = {"text": query, "per_page": count}
        data = self._connect_to_api(params)
        if isinstance(data, dict):
            return data.get("items", [])
        return []

    def get_employers_by_ids(self, employer_ids: List[int]) -> List[dict]:
        """Возвращает данные о работодателях по их ID."""
        employers = []
        for emp_id in employer_ids:
            try:
                response = requests.get(f"https://api.hh.ru/employers/{emp_id}", timeout=10)
                response.raise_for_status()
                employers.append(response.json())
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при получении работодателя {emp_id}: {e}")
        return employers

    def get_vacancies_by_employer(self, employer_id: int, count: int = 10) -> List[dict]:
        """Возвращает вакансии, опубликованные заданным работодателем."""
        params = {"employer_id": employer_id, "per_page": count}
        data = self._connect_to_api(params)
        if isinstance(data, dict):
            return data.get("items", [])
        return []