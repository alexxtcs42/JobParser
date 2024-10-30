import requests
import sqlite3
from pywebio import input, output, start_server


def get_vacancies(keyword):
    conn = sqlite3.connect('db/parser_database.db')
    c = conn.cursor()

    url = "https://api.hh.ru/vacancies"

    for p in range(20):
        params = {
            "text": keyword,
            "per_page": 100,
            "page": p
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Chrome/64.0.3282.186',
        }

        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            vacancies = data.get("items", [])
            num_vacancies = len(vacancies)

            if num_vacancies > 0:
                for i, vacancy in enumerate(vacancies):
                    vacancy_id = vacancy.get("id")
                    if c.execute(f"SELECT * FROM job_openings WHERE id = {vacancy_id}"):
                        continue
                    vacancy_title = vacancy.get("name")
                    vacancy_url = vacancy.get("alternate_url")

                    employer = vacancy.get("employer", {})
                    company_name = None
                    if employer:
                        company_name = employer.get("name")

                    salary = vacancy.get("salary", {})
                    salary_from, salary_to, salary_currency = None, None, None
                    if salary:
                        salary_from = salary.get("from")
                        salary_to = salary.get("to")
                        salary_currency = salary.get("currency")

                    area_name = None
                    area = vacancy.get("area", {})
                    if area:
                        area_name = area.get("name")

                    is_archived = vacancy.get("archived")

                    working_days, working_time_intervals, working_time_modes = None, None, None
                    days = vacancy.get("working_days", {})
                    if days:
                        working_days = days[0].get("name")
                    time_intervals = vacancy.get("working_time_intervals", {})
                    if time_intervals:
                        working_time_intervals = time_intervals[0].get("name")
                    time_modes = vacancy.get("working_time_modes", {})
                    if time_modes:
                        working_time_modes = time_modes[0].get("name")

                    experience, employment = None, None
                    exp = vacancy.get("experience", {})
                    if exp:
                        experience = exp.get("name")
                    emp = vacancy.get("employment", {})
                    if emp:
                        employment = emp.get("name")

                    c.execute(f"INSERT INTO job_openings (id, url, vacancy_title, employer, area, "
                              f"salary_from, salary_to, salary_currency, is_archived, "
                              f"working_days, time_intervals, time_modes, experience, employment) "
                              f"VALUES ({vacancy_id}, {vacancy_url}, {vacancy_title}, {company_name}, {area_name}, "
                              f"{salary_from}, {salary_to}, {salary_currency}, {is_archived}, "
                              f"{working_days}, {working_time_intervals}, {working_time_modes}, "
                              f"{experience}, {employment})")
                    conn.commit()
            elif p == 0:
                output.put_text("Вакансий не найдено :(")
        else:
            output.put_text(f"Ошибка {response.status_code}")
            break
    conn.commit()
    conn.close()
    return None


def print_vacancies(title, employer, area, exp, emp, from_, to, currency, days, intervals, modes, archived):
    conn = sqlite3.connect('db/parser_database.db')
    c = conn.cursor()
    vacancies = c.execute(f"SELECT * from job_openings WHERE "
                          f"({title} IN vacancy_title) AND "
                          f"({employer} IN employer) AND "
                          f"({area} IN area) AND "
                          f"({exp} IN experience) AND "
                          f"({emp} IN employment) AND "
                          f"({from_} < salary_to) AND "
                          f"({to} > salary_from) AND "
                          f"({currency} = salary_currency)")
    conn.commit()
    conn.close()
    if vacancies:
        for vacancy in vacancies:
            print(vacancy)
            # output.put_text(f"ID: {vacancy_id}")
            # output.put_text(f"Вакансия: {vacancy_title if vacancy_title else 'Без названия'}")
            # output.put_text(f"Работодатель: {company_name if company_name else 'Неизвестен'}")
            # if salary_from and salary_to:
            #     output.put_text(f"Зарплата: от {salary_from} до {salary_to} {salary_currency if salary_currency else 'денег'}")
            # elif salary_from:
            #     output.put_text(f"Зарплата: от {salary_from} {salary_currency if salary_currency else 'денег'}")
            # elif salary_to:
            #     output.put_text(f"Зарплата: до {salary_to} {salary_currency if salary_currency else 'денег'}")
            # else:
            #     output.put_text(f"Зарплата: неизвестна")
            # output.put_text(f"Населённый пункт: {area_name if area_name else 'любой'}")
            # output.put_text(f"По субботам и воскресеньям: {'да' if working_days else 'нет'}")
            # output.put_text(f"Можно сменами по 4-6 часов в день: {'да' if working_time_intervals else 'нет'}")
            # output.put_text(f"С началом дня после 16:00: {'да' if working_time_modes else 'нет'}")
            # output.put_text(f"Опыт: {experience if experience else 'Нет опыта'}")
            # output.put_text(f"Занятость: {employment if employment else 'Неизвестно'}")
            # output.put_text(f"Архивирована: {'да' if is_archived == 'true' else 'нет'}")
            # output.put_text(f"URL: {vacancy_url}")
            output.put_text("")
            output.put_text("---------")
    else:
        output.put_text("Вакансий не найдено :(")
    return None


def search_vacancies():
    keyword = input.input("Введите ключевое слово для поиска вакансии: ", type=input.TEXT)
    title_input = input.input("Название вакансии: ", type=input.TEXT)
    employer_input = input.input("Работодатель: ", type=input.TEXT)
    area_input = input.input("Населённый пункт: ", type=input.TEXT)
    experience_input = input.input("Опыт работы: ", type=input.TEXT)
    employment_input = input.input("Вид занятости: ", type=input.TEXT)
    from_input = input.input("Зарплата от ", type=input.NUMBER)
    to_input = input.input("до", type=input.NUMBER)
    currency_input = input.input("Валюта (RUR - рубли, USD - доллары и т. д.): ", type=input.TEXT)
    days_input = input.checkbox("Работа по: ", options=['будням', 'субботам и воскресеньям'])
    intervals_input = input.checkbox("Сменами по 4-6 часов в день: ", options=['да', 'нет'])
    modes_input = input.checkbox("Начало дня: ", options=['до 16:00', 'после 16:00'])
    archived_input = input.checkbox("Показать архивированные: ", options=['нет', 'только архивированные'])
    output.clear()
    get_vacancies(keyword)
    print_vacancies(title_input, employer_input, area_input, experience_input, employment_input,
                    from_input, to_input, currency_input, days_input, intervals_input, modes_input, archived_input)
    return None


if __name__ == '__main__':
    start_server(search_vacancies, port=8080)
