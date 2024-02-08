from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import date
import pandas
import collections


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
    excel_spreadsheet_of_wine = pandas.read_excel('wine.xlsx', sheet_name='Лист1', na_values=['N/A', 'NA'], keep_default_na=False)
    all_products = excel_spreadsheet_of_wine.to_dict(orient='records')

    drinks = []
    white_wine = []
    red_wine = []
    all_drinks = collections.defaultdict(list)
    for product in all_products:
        category = product['Категория']
        if category == 'Белые вина':
            white_wine.append(product)
            all_drinks[category] = white_wine
        elif category == 'Красные вина':
            red_wine.append(product)
            all_drinks[category] = red_wine
        else:
            drinks.append(product)
            all_drinks[category] = drinks

    today_s_date = date.today()
    years = today_s_date.year - 1920

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
