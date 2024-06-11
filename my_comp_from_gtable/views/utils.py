import pandas as pd
import time
import requests

import settings
from my_call_load.models.models import CallInfo

OBJECT_CRM = {"Лиды": '1',
              "Сделки": '2',
              "Контакты": '3',
              "Компании": '4',
              "Коммерческие предложения": '7',
              "Новые счета": '31'}


def get_data_by_link(link, prepare=True):
    if prepare:
        link = "/".join(link.split("/")[:-1]) + "/export"

    file = pd.ExcelFile(link)
    sheets = file.sheet_names

    data = [file.parse(sheet_name=i) for i in sheets]
    data = [df.to_dict('records') for df in data]

    result = []
    for name, item in zip(sheets, data):
        result.append(
            {
                'NAME': name,
                'DATA': item
            }
        )
    return result


def get_prefix(_id):
    return f'{time.time()}_{_id}'


def _get_mod_data(data, field):
    for item in data:
        if item.get(field):
            new_value = get_prefix(item[field])
            item[field] = new_value
    return data


def _add_crm(but, item):

    helper = {
        'Компании': 'ORIGIN_ID',
        'Контакты': 'COMPANY_ORIGIN_ID'
    }

    type_id = OBJECT_CRM[item['NAME']]
    data = item['DATA']

    # Проверяем на наличие связей. Если есть - модифицируем индексы
    if item['NAME'] in ('Компании', 'Контакты'):
        data = _get_mod_data(data, field=helper[item['NAME']])

    # При добавлении через батч стоит ограничение в 20 штук
    batch = []
    while data:
        batch.append(data[:20])
        data = data[20:]

    for i in batch:
        but.call_api_method('crm.item.batchImport', {'entityTypeId': type_id, 'data': i})  # Ограничение - 20 сущностей!!!
    return item['NAME'], len(item['DATA'])


def _add_call(but, data):
    for ring in data['DATA']:
        # Получаем файл
        link = ''  # https://drive.usercontent.google.com/u/0/uc?id=17Z9Hnma4rCmI1S4dKHXDH0lIT62_uHbZ&export=download
        file = None
        if ring.get('file'):
            link = ring['file']

            # https://drive.google.com/uc?id=YOUR_FILE_ID_HERE&export=download
            file_id = link.split('/')[-2]
            link = 'https://drive.google.com/uc?id=' + file_id + '&export=download'
            file = requests.get(url=link).content

            temp_name = f"temp_ring_{str(time.time()).replace('.', '')}.mp3"
            file_path = f'{settings.MEDIA_ROOT}/{temp_name}'
            with open(file_path, "wb") as f:
                f.write(file)

            ring['file'] = temp_name

        call = CallInfo(**ring)
        call.telephony_externalcall_register(but)
        call.telephony_externalcall_finish(but)
        if link:
            call.telephony_externalcall_attach_record(but)

    return data['NAME'], len(data['DATA'])


class B24Loader:
    items = {
        'Компании': _add_crm,
        'Контакты': _add_crm,
        'Сделки': _add_crm,
        'Лиды': _add_crm,
        'Звонки': _add_call,
    }

    @classmethod
    def add_to_bitrix(cls, but, items):
        info = []
        for item in items:
            command = cls.items[item['NAME']]
            temp = command(but, item)
            info.append(temp)
        return info

