import datetime
import pandas
from pprint import pprint
from jinja2 import Environment, FileSystemLoader, select_autoescape
from http.server import HTTPServer, SimpleHTTPRequestHandler

today = datetime.datetime.now()
current_year = today.year

excel_data_df = pandas.read_excel('wine.xlsx', sheet_name='Лист1')
wines = excel_data_df.to_dict(orient='record')
pprint(wines)


def get_age(current_year):
    foundation_date = 1920
    past_years = current_year - foundation_date
    return f'Уже {past_years} год с вами'


winery_age = get_age(current_year)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    winery_age=winery_age
)

with open('index.html', 'w', encoding='utf8') as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
