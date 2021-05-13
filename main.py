import datetime
import pandas
import collections
from collections import OrderedDict
from jinja2 import Environment, FileSystemLoader, select_autoescape
from http.server import HTTPServer, SimpleHTTPRequestHandler


def get_age(current_year):
    foundation_date = 1920
    lifetime = current_year - foundation_date
    return f'Уже {lifetime} год с вами'


if __name__ == '__main__':
    today = datetime.datetime.now()
    current_year = today.year

    winery_age = get_age(current_year)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    wines_from_excel = pandas.read_excel(
        'wines.xlsx',
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
