import random


crm_fields = {'Лиды': {'command': 'crm.lead.list', 'field': 'NAME'},
              'Компании': {'command': 'crm.company.list', 'field': 'TITLE'},
              'Контакты': {'command': 'crm.contact.list', 'field': 'NAME'},
              'Товары': {'command': 'crm.product.property.list', 'field': 'NAME'}}


def get_data_for_choice():
    return ((key,  key) for key in crm_fields.keys())


def get_duplicate(but, field):
    # получаем список сущностей
    target = crm_fields[field]
    list_target = but.call_list_method(target['command'])

    # === ищем дубликаты ===
    item = target['field']
    list_target = [(crm[item], crm['ID']) for crm in list_target]

    temp_dict = {}
    # {'count': int, 'IDs': []}
    # считаем все значения
    for crm in list_target:
        item, _id = crm
        if temp_dict.get(item):
            temp_dict[item]['count'] += 1
            temp_dict[item]['IDs'].append(_id)
        else:
            temp_dict[item] = {'count': 1, 'IDs': [_id]}

    # оставляем только неуникальные значения
    result = []
    for k, v in temp_dict.items():
        if v['count'] > 1:
            result.append(
                {
                    'field': k,
                    'count': v['count'],
                    'IDs': ', '.join(v['IDs'])
                }
            )

    return result


'''
# добавление фейковых контактов для проверки работоспособности
def add_fake_contacts(but, count):
    names = ['John', 'Vasya', 'Mary', 'Oz']
    second_names = ['Ivanov', 'Smidth', 'Lermontov', 'Black']

    for _ in range(count):
        fields = {
            'NAME': random.choice(names),
            'SECOND_NAME': random.choice(second_names)
        }

        but.call_api_method('crm.contact.add', {'fields': fields})
'''
