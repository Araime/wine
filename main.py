import datetime
import pandas
import collections
import argparse
from collections import OrderedDict
from jinja2 import Environment, FileSystemLoader, select_autoescape
from http.server import HTTPServer, SimpleHTTPRequestHandler


def get_age(current_year):
    foundation_year = 1925
    age_of_the_winery = current_year - foundation_year
    return age_of_the_winery


def get_correct_word(age):
    if age % 10 == 1 and age != 11 and age % 100 != 11:
        word = 'год'
    elif 1 < age % 10 <= 4 and age != 12 and age != 13 and age != 14:
        word = 'года'
    else:
        word = 'лет'
    return word


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Программа принимает файл в формате xlsx'
                                                 ' для отображения на сайте', )
    parser.add_argument('file_path', help='Необходимо в качестве аргумента при запуске указать'
                                          ' полный путь к файлу')
    args = parser.parse_args()
    path_to_the_table = args.file_path

    today = datetime.datetime.now()
    current_year = today.year
    age = get_age(current_year)
    correct_word = get_correct_word(age)
    winery_age = f'Уже {age} {correct_word} с вами'

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    wines_from_table = pandas.read_excel(
        path_to_the_table,
        sheet_name='Лист1',
        na_values=' ',
        keep_default_na=False
    )

    wines_table_to_dict = wines_from_table.to_dict(orient='records')
    grouped_wines = collections.defaultdict(list)
    for wine in wines_table_to_dict:
        key = wine.get('Категория')
        grouped_wines[key].append(wine)

    ordered_wines = OrderedDict(sorted(grouped_wines.items()))

    template = env.get_template('template.html')
    rendered_page = template.render(
        winery_age=winery_age,
        ordered_wines=ordered_wines
    )

    with open('index.html', 'w', encoding='utf8') as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
