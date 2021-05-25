import datetime
import pandas
import collections
import argparse
from collections import OrderedDict
from jinja2 import Environment, FileSystemLoader, select_autoescape
from http.server import HTTPServer, SimpleHTTPRequestHandler


def get_age(foundation_year):
    today = datetime.datetime.now()
    current_year = today.year
    age_of_the_winery = current_year - foundation_year
    return age_of_the_winery


def get_years_caption(age):
    if age % 10 == 1 and age != 11 and age % 100 != 11:
        word = 'год'
    elif 1 < age % 10 <= 4 and age != 12 and age != 13 and age != 14:
        word = 'года'
    else:
        word = 'лет'
    return word


def get_ordered_wines(path_to_file):
    wines_from_file = pandas.read_excel(
        path_to_file,
        sheet_name='Лист1',
        na_values=' ',
        keep_default_na=False
    ).to_dict(orient='records')

    products = collections.defaultdict(list)
    for wine in wines_from_file:
        key = wine.get('Категория')
        products[key].append(wine)

    ordered_products = OrderedDict(sorted(products.items()))
    return ordered_products


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Программа принимает файл в формате xlsx'
                                                 ' для отображения на сайте', )
    parser.add_argument('file_path', help='Необходимо в качестве аргумента при запуске указать'
                                          ' полный путь к файлу')
    args = parser.parse_args()
    path_to_file = args.file_path

    foundation_year = 1920
    age = get_age(foundation_year)
    age_in_years = get_years_caption(age)
    age_label = f'Уже {age} {age_in_years} с вами'

    ordered_wines = get_ordered_wines(path_to_file)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    rendered_page = template.render(
        age_label=age_label,
        ordered_wines=ordered_wines
    )

    with open('index.html', 'w', encoding='utf8') as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
