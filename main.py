from hh_salaries import get_hh_data_by_language
from superjob_vacancies import get_sj_data_by_language
from terminaltables import AsciiTable


def add_to_table(table_data, data_by_language):
    table_data.append(
        [
            language,
            data_by_language['vacancies_found'],
            data_by_language['vacancies_processed'],
            data_by_language['average_salary']
        ]
    )


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

    hh_table_data = [['Язык программирования', 'Вакансий найдено',
                      'Вакансий обработано', 'Средняя зарплата']]
    sj_table_data = hh_table_data.copy()

    for language in languages:
        add_to_table(hh_table_data, get_hh_data_by_language(language))
        add_to_table(sj_table_data, get_sj_data_by_language(language))

    table = AsciiTable(hh_table_data)
    table.title = 'HeadHunter Moscow'
    print(table.table)

    # print(json.dumps(data_by_languages, indent=4))
    table = AsciiTable(sj_table_data)
    table.title = 'SuperJob Moscow'
    print(table.table)
