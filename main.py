from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import date
import pandas
import collections
import argparse


def do_right_years(years):
    remainder_of_integer = years % 100
    if remainder_of_integer > 14:
        remainder_of_integer = remainder_of_integer % 10
    if remainder_of_integer == 1:
        name_of_year = 'год'
    elif remainder_of_integer > 1 and remainder_of_integer < 5:
        name_of_year = 'года'
    else:
        name_of_year = 'лет'
    return name_of_year


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Выбор xlsx файла для выгрузки товаров на сайт, по-умолчанию выбран wine.xlsx файл'
    )
    parser.add_argument("--file_name", help="Название xlsx файла для выгрузки товаров на сайт", type=str, default='wine.xlsx')
    args = parser.parse_args()
    file_name = args.file_name

    excel_spreadsheet_of_wine = pandas.read_excel(file_name, sheet_name='Лист1', na_values=['N/A', 'NA'], keep_default_na=False)
    all_products = excel_spreadsheet_of_wine.to_dict(orient='records')

    all_drinks = collections.defaultdict(list)
    for product in all_products:
        category = product['Категория']
        all_drinks[category].append(product)

    date_of_the_start_of_sales = 1920
    today_s_date = date.today()
    years = today_s_date.year - date_of_the_start_of_sales

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        years=years,
        name_of_year=do_right_years(years),
        all_drinks=all_drinks
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
