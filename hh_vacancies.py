import requests
import time

from statistics import mean
from itertools import count
from salaries import predict_salary


def predict_rub_salary_hh(vacancies):
    salary_by_language = {}

    predicted_salaries = []

    for vacancy in vacancies:
        salary = vacancy['salary']
        if not salary or salary['currency'] != 'RUR':
            continue

        predicted_salary = predict_salary(salary['from'], salary['to'])
        if predicted_salary:
            predicted_salaries.append(predicted_salary)

    salary_by_language['vacancies_processed'] = len(predicted_salaries)
    salary_by_language['average_salary'] = int(mean(predicted_salaries))

    return salary_by_language


def get_all_hh_vacancies(url, params):
    all_vacancies = []
    for page in count(0):
        params['page'] = page
        response = requests.get(url, params)
        response.raise_for_status()
        vacancies = response.json()['items']
        while True:
            try:
                for vacancy in vacancies:
                    all_vacancies.append(vacancy)
                break
            except ConnectionError:
                print('Пытаюсь восстановить подключение...')
                time.sleep(5)

        if page >= response.json()['pages']:
            break

    return all_vacancies, response.json()['found']


def get_hh_salary_by_language(language):
    hh_base_url = 'https://api.hh.ru/vacancies'
    vacancies_per_page = 100

    params = {
        'text': f'Программист {language}',
        'area': '1',
        'only_with_salary': True,
        'per_page': vacancies_per_page
    }

    print('Загружаю вакансии HH по запросу "{0}"'.format(params['text']))
    vacancies, found = get_all_hh_vacancies(hh_base_url, params)

    salary_by_language = predict_rub_salary_hh(vacancies)
    salary_by_language['vacancies_found'] = found

    return salary_by_language
