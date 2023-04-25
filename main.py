import os

from hh_vacancies import get_hh_salary_by_language
from superjob_vacancies import get_sj_salary_by_language
from terminaltables import AsciiTable
from dotenv import load_dotenv


def add_to_table(table_content, salary_by_language):
    table_content.append(
        [
            language,
            salary_by_language['vacancies_found'],
            salary_by_language['vacancies_processed'],
            salary_by_language['average_salary']
        ]
    )


def show_table(table_content, table_name):
    table = AsciiTable(table_content)
    table.title = table_name
    print(table.table)


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
    load_dotenv()
    headers = {
        'X-Api-App-Id': os.environ['SUPERJOB_TOKEN'],
    }

    hh_table_content = [['Язык программирования', 'Вакансий найдено',
                         'Вакансий обработано', 'Средняя зарплата']]
    sj_table_content = hh_table_content.copy()

    for language in languages:
        add_to_table(hh_table_content, get_hh_salary_by_language(language))
        add_to_table(sj_table_content, get_sj_salary_by_language(language, headers))

    show_table(hh_table_content, 'HeadHunter Moscow')
    show_table(sj_table_content, 'SuperJob Moscow')
