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


def predict_rub_salary(salary):
    # salary = vacancy['salary']
    if not salary or salary['currency'] != 'RUR':
        return None
    if not salary['from']:
        return int(salary['to']) * 0.8
    if not salary['to']:
        return int(salary['from']) * 1.2
    return int((int(salary['from']) + int(salary['from']))/2)


def extract_data(salaries):
    data_by_language = {}

    predicted_salaries = []

    for salary in salaries:
        predicted_salary = predict_rub_salary(salary)
        if predicted_salary:
            predicted_salaries.append(predicted_salary)

    #data_by_language['vacancies_found:'] = response.json()['found']
    data_by_language['vacancies_processed:'] = len(predicted_salaries)
    data_by_language['average_salary:'] = int(mean(predicted_salaries))

    return data_by_language


def get_all_salaries(url, params):
    salaries = []
    for page in count(0):
        params['page'] = page
        response = requests.get(url, params)
        response.raise_for_status()
        vacancies = response.json()['items']
        for vacancy in vacancies:
            salaries.append(vacancy['salary'])
        print(f'Загрузил страницу {page}')

        if page >= response.json()['pages']:
            break

    return salaries, response.json()['found']


if __name__ == '__main__':
    languages = [
        'JavaScript',
        'Java',
        'Python',
        'Ruby',
        'PHP',
        'C++',
        'C#',
        'C ',
    ]
    data_by_languages = {}

    hh_base_url = 'https://api.hh.ru/vacancies'

    for language in languages:
        params = {
            'text': f'Программист {language}',
            'area': '1',
            'only_with_salary': True,
            'per_page': 100
        }
        headers = {'User-Agent': 'boltasov-app/0.0.1 alexandr.boltasov@gmail.com'}

        print(f'Загружаю язык {language}')
        salaries, found = get_all_salaries(hh_base_url, params)

        data_by_languages[language] = extract_data(salaries)
        data_by_languages[language]['vacancies_found:'] = found

        time.sleep(5)

    print(json.dumps(data_by_languages, indent=4))
