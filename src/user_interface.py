from src.db_manager import DBManager


def user_menu() -> None:
    """Выводит меню взаимодействия с пользователем и обрабатывает ввод."""
    db = DBManager()
    while True:
        print(
            """
        1 - Показать компании и количество вакансий
        2 - Показать все вакансии
        3 - Показать среднюю зарплату
        4 - Вакансии с зарплатой выше средней
        5 - Поиск вакансий по ключевому слову
        0 - Выход
        """
        )
        choice = input("Выберите действие: ")

        if choice == "1":
            for row in db.get_companies_and_vacancies_count():
                print(f"{row[0]} — {row[1]} вакансий")
        elif choice == "2":
            for row in db.get_all_vacancies():
                print(f"{row[0]} | {row[1]} | от {row[2]} до {row[3]} | {row[4]}")
        elif choice == "3":
            print(f"Средняя зарплата: {db.get_avg_salary():.2f}")
        elif choice == "4":
            for row in db.get_vacancies_with_higher_salary():
                print(f"{row[0]} | от {row[1]} до {row[2]} | {row[3]}")
        elif choice == "5":
            keyword = input("Введите ключевое слово: ")
            for row in db.get_vacancies_with_keyword(keyword):
                print(f"{row[0]} | от {row[1]} до {row[2]} | {row[3]}")
        elif choice == "0":
            db.close()
            break
        else:
            print("Неверный выбор, попробуйте снова")
