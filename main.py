from src.api_hh import HeadHunterAPI
from src.db_creator import create_database, create_tables
from src.db_filler import insert_employers, insert_vacancies
from src.user_interface import user_menu

EMPLOYER_IDS = [80, 3529, 15478, 78638, 1740, 1122462, 3388, 2180, 1057, 1455]

if __name__ == "__main__":
    create_database()
    create_tables()

    hh = HeadHunterAPI()
    employers = hh.get_employers_by_ids(EMPLOYER_IDS)
    insert_employers(employers)

    for emp_id in EMPLOYER_IDS:
        vacancies = hh.get_vacancies_by_employer(emp_id)
        insert_vacancies(emp_id, vacancies)

    user_menu()
