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
    
    excel_data_df_wine3 = pandas.read_excel(
    'wine3.xlsx', sheet_name='Лист1',
    na_values=['N/A', 'NA'], keep_default_na=False
    )
    all_products = excel_data_df_wine3.to_dict(orient='records')

    list_drinks = []
    list_white_wine = []
    list_red_wine = []
    dict_of_all_drinks=collections.defaultdict(list)
    for product in all_products:
        category = product['Категория']
        if category == 'Белые вина':
            list_white_wine.append(product)
            dict_of_all_drinks[category] = list_white_wine
        elif category == 'Красные вина':
            list_red_wine.append(product)
            dict_of_all_drinks[category] = list_red_wine
        else:
            list_drinks.append(product)
            dict_of_all_drinks[category] = list_drinks

    first_date = date(1920, 1, 1)
    second_date = date.today()
    years = second_date.year - first_date.year

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        years=years,
        name_of_year=do_right_years(years),
        dict_of_all_drinks=dict_of_all_drinks
    )


    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
        
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
