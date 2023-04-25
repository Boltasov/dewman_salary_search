import requests
import time

from statistics import mean
from itertools import count
from salaries import predict_salary


def predict_rub_salary_sj(vacancies):
    salary_by_language = {}

    predicted_salaries = []

    for vacancy in vacancies:
        salary_from = vacancy['payment_from']
        salary_to = vacancy['payment_to']
        if (not salary_from and not salary_to) or vacancy['currency'] != 'rub':
            continue

        predicted_salary = predict_salary(salary_from, salary_to)
        if predicted_salary:
            predicted_salaries.append(predicted_salary)

    salary_by_language['vacancies_processed'] = len(predicted_salaries)
    salary_by_language['average_salary'] = int(mean(predicted_salaries))

    return salary_by_language


def get_all_sj_vacancies(url, params, headers):
    all_vacancies = []
    for page in count(0):
        params['page'] = page
        while True:
            try:
                response = requests.get(url, params=params, headers=headers)
                response.raise_for_status()
                break
            except ConnectionError:
                print('Пытаюсь восстановить подключение...')
                time.sleep(5)

        vacancies = response.json()['objects']
        for vacancy in vacancies:
            all_vacancies.append(vacancy)

        if not vacancies['more']:
            break

    return all_vacancies, vacancies['total']


def get_sj_salary_by_language(language, headers):
    superjob_url = 'https://api.superjob.ru/2.0/vacancies/'
    vacancies_per_page = 100
    moscow_city_code = 4
    it_catalogue_id = 48

    params = {
        'catalogues': it_catalogue_id,
        'town': moscow_city_code,
        'keyword': f'Программист {language}',
        'count': vacancies_per_page
    }

    print('Загружаю вакансии SJ по запросу "{0}"'.format(params['keyword']))

    vacancies, total = get_all_sj_vacancies(superjob_url, params, headers)

    salary_by_language = predict_rub_salary_sj(vacancies)
    salary_by_language['vacancies_found'] = total

    return salary_by_language
