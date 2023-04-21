import requests
import os
import json
import codecs
import time

from statistics import mean
from itertools import count
from dotenv import load_dotenv


def predict_rub_salary_sj(vacancy):
    min_salary = vacancy['payment_from']
    max_salary = vacancy['payment_to']
    if (not min_salary and not max_salary) or vacancy['currency'] != 'rub':
        return None
    if not min_salary:
        return int(max_salary) * 0.8
    if not max_salary:
        return int(min_salary) * 1.2
    return int((int(min_salary) + int(max_salary)) / 2)


def save_to_file(response, file_name):
    with codecs.open(file_name, 'w', 'utf-8') as json_file:
        json.dump(response.json(), json_file, indent=4, sort_keys=True)


if __name__ == '__main__':
    superjob_url = 'https://api.superjob.ru/2.0/vacancies/'

    load_dotenv()
    headers = {
        'X-Api-App-Id': os.environ['SUPERJOB_TOKEN'],
    }
    params = {
        'catalogues': 48,
        'town': 4,
    }

    response = requests.get(superjob_url, headers=headers, params=params)
    response.raise_for_status()

    save_to_file(response, 'vacancies_sj.json')

    vacancies = response.json()['objects']
    for vacancy in vacancies:
        salary = predict_rub_salary_sj(vacancy)
        print("{0}, {1}, {2}]".format(vacancy['profession'], vacancy['town']['title'], salary))
