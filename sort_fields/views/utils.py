import locale
from django import forms


def get_choices(fields: list):
    choices = []
    for field in fields:
        try:
            info = field['SETTINGS']
            display = info['DISPLAY']
            if display == 'LIST':
                choices.append((field['ID'], field['FIELD_NAME']))
        except:
            pass
    return choices


def get_form(choices):
    class ListForm(forms.Form):
        id = forms.ChoiceField(choices=choices, label='Выберите путь поля')

    return ListForm


def get_sorted_list(arr: list):
    locale.setlocale(locale.LC_ALL, '')
    sorted_data = sorted(arr, key=lambda x: locale.strxfrm(x['VALUE']))

    for i in range(len(sorted_data)):
        sorted_data[i]['SORT'] = i + 1

    return sorted_data


def do_sort(but, field_id):
    try:
        # Получаем список из поля по его ID
        field = but.call_api_method('crm.company.userfield.get', {'id': field_id})['result']
        field_list = field['LIST']

        # Сортировка и обновление поля SORT
        sorted_list = get_sorted_list(field_list)
        for i in sorted_list:
            print(i)

        # апдейт списка
        but.call_api_method('crm.company.userfield.update', {'id': field_id, 'fields': {'LIST': sorted_list}})
        return 'Поле успешно отсортировано'
    except Exception as ex:
        print(ex)
        return 'Произошла ошибка, попробуйте позже'
