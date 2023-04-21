import requests
import os
import json
import codecs
from statistics import mean
from itertools import count
import time
from hh_salaries import get_hh_data_by_language


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

    for language in languages:
        data_by_languages[language] = get_hh_data_by_language(language)

    print(json.dumps(data_by_languages, indent=4))
