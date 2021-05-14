import datetime
import pandas
import collections
import argparse
from collections import OrderedDict
from jinja2 import Environment, FileSystemLoader, select_autoescape
from http.server import HTTPServer, SimpleHTTPRequestHandler


def get_age(current_year):
    foundation_date = 1920
    lifetime = current_year - foundation_date
    return f'Уже {lifetime} год с вами'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Программа принимает файл в формате xlsx'
                                                 ' для отображения на сайте', )
    parser.add_argument('file_path', help='Необходимо в качестве аргумента при запуске указать'
                                          ' полный путь к файлу')
    args = parser.parse_args()
    excel_file = args.file_path

    today = datetime.datetime.now()
    current_year = today.year
    winery_age = get_age(current_year)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    wines_from_excel = pandas.read_excel(
        excel_file,
        sheet_name='Лист1',
        na_values=' ',
        keep_default_na=False
    )

    wines_converted_to_dictionary = wines_from_excel.to_dict(orient='record')
    grouped_wines = collections.defaultdict(list)
    for wine in wines_converted_to_dictionary:
        key = wine.get('Категория')
        grouped_wines[key].append(wine)

    sorted_by_order_of_wine = OrderedDict(sorted(grouped_wines.items()))

    template = env.get_template('template.html')
    rendered_page = template.render(
        winery_age=winery_age,
        sorted_by_order_of_wine=sorted_by_order_of_wine
    )

    with open('index.html', 'w', encoding='utf8') as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
