import datetime
import pandas
import collections
import argparse
from collections import OrderedDict
from jinja2 import Environment, FileSystemLoader, select_autoescape
from http.server import HTTPServer, SimpleHTTPRequestHandler


def get_age(current_year):
    foundation_date = 1920
    how_old_is_the_winery = current_year - foundation_date
    return f'Уже {how_old_is_the_winery} год с вами'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Программа принимает файл в формате xlsx'
                                                 ' для отображения на сайте', )
    parser.add_argument('file_path', help='Необходимо в качестве аргумента при запуске указать'
                                          ' полный путь к файлу')
    args = parser.parse_args()
    prepared_table_with_wines = args.file_path

    today = datetime.datetime.now()
    current_year = today.year
    winery_age = get_age(current_year)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    derived_from_excel_wines = pandas.read_excel(
        prepared_table_with_wines,
        sheet_name='Лист1',
        na_values=' ',
        keep_default_na=False
    )

    wines_converted_to_dictionary = derived_from_excel_wines.to_dict(orient='record')
    grouped_wines = collections.defaultdict(list)
    for wine in wines_converted_to_dictionary:
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
