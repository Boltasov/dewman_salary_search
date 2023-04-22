import requests
import os
import json
import codecs
from statistics import mean
from itertools import count
import time


def save_to_file(response, file_name):
    with codecs.open(file_name, 'w', 'utf-8') as json_file:
        json.dump(response.json(), json_file, indent=4, sort_keys=True)


def predict_salary(salary_from: int, salary_to: int):
    if not salary_from:
        return int(salary_to * 0.8)
    if not salary_to:
        return int(salary_from * 1.2)
    return int((salary_from + salary_to)/2)


def predict_rub_salary_hh(vacancies):
    data_by_language = {}

    predicted_salaries = []

    for vacancy in vacancies:
        salary = vacancy['salary']
        if not salary or salary['currency'] != 'RUR':
            continue

        predicted_salary = predict_salary(salary['from'], salary['to'])
        if predicted_salary:
            predicted_salaries.append(predicted_salary)

    data_by_language['vacancies_processed'] = len(predicted_salaries)
    data_by_language['average_salary'] = int(mean(predicted_salaries))

    return data_by_language


def get_all_vacancies(url, params):
    all_vacancies = []
    for page in count(0):
        params['page'] = page
        response = requests.get(url, params)
        response.raise_for_status()
        vacancies = response.json()['items']
        for vacancy in vacancies:
            all_vacancies.append(vacancy)
        print(f'Загрузил страницу {page}')

        # if page >= response.json()['pages']:
        if page >= 1:
            break

    return all_vacancies, response.json()['found']


def get_hh_data_by_language(language):
    hh_base_url = 'https://api.hh.ru/vacancies'

    params = {
        'text': f'Программист {language}',
        'area': '1',
        'only_with_salary': True,
        'per_page': 100
    }

    print('Загружаю вакансии HH по запросу "{0}"'.format(params['text']))
    vacancies, found = get_all_vacancies(hh_base_url, params)

    data_by_language = predict_rub_salary_hh(vacancies)
    data_by_language['vacancies_found'] = found

    return data_by_language
