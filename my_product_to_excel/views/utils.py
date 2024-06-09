from django import forms
from datetime import datetime as dt
import pandas as pd


def date_parse(products):

    dates_dict = dict()
    for product in products:
        dates_dict[product["ID"]] = product["DATE_CREATE"]
    for key, date in dates_dict.items():
        res = dt.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
        formatted_date = res.strftime("%d.%m.%Y %H:%M:%S")
        dates_dict[key] = formatted_date

    return dates_dict


def users_in_dict(users):

    users_dict = dict()
    for user in users:
        users_dict[user["ID"]] = f'{user["NAME"]} {user["LAST_NAME"]}'

    return users_dict


class ProductManager:
    """ Работа с продуктами, выгрузка в Excel """

    data = [
        ["ID", "Название", "Код товара", "Дата создания", "Кем изменено", "Кем создано", "ID каталога",
         "Описание товара", "Цена", "Валюта"],
    ]

    def __init__(self, but):
        self.but = but
        self.products = []
        self.choices = {}

        self._find_all_products()
        self._create_choices()

    def _find_all_products(self):
        self.products = self.but.call_list_method('crm.product.list')

    def _create_choices(self):
        codes = [i['CODE'] for i in self.products]
        codes = set(codes)
        codes = ['Вывести для всех'] + sorted(list(codes))
        self.choices = {str(i): codes[i] for i in range(len(codes))}

    def get_form(self):
        class ChoiceCode(forms.Form):
            code = forms.ChoiceField(choices=self.choices.items(),
                                     label='Выберите категорию (код) товара')
        return ChoiceCode

    def save_and_get_path(self, choice):
        users = self.but.call_list_method('user.get')
        users_name = users_in_dict(users)

        # выбираем продукты по коду
        products = []
        if choice == '0':
            products = self.products
        else:
            code = self.choices[choice]
            products = [i for i in self.products if i['CODE'] == code]

        date = date_parse(products)

        data = self.data[:]
        for product in products:
            data.append([product['ID'], product['NAME'], product['CODE'], date[product['ID']],
                         users_name[product['MODIFIED_BY']], users_name[product['CREATED_BY']], product['CATALOG_ID'],
                         product['DESCRIPTION'], product['PRICE'], product['CURRENCY_ID']])

        df = pd.DataFrame(data)

        path_date = dt.now().strftime("%d_%m_%Y_%H_%M_%S")
        path = f'tempfiles/temp_products_{path_date}.xlsx'
        df.to_excel(path, index=False, header=False)

        return path

