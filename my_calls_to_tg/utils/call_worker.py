from .options import Option
from .utils import upload_calls
from .threads import new_thread


def add_all(but, token, chat_id):
    option = Option(but)
    item = option.find(token, chat_id)

    if not item:
        item = {'token': token,
                'chat_id': chat_id,
                'auto': 'False',
                'last_call_id': '0'}
    else:
        item = item[0]

    if item['auto'] == 'True':
        return 'Для данного чата звонки выгружаются автоматически'

    result = upload_calls(but, item)
    if result['change_id']:
        item['last_call_id'] = result['last_id']
        option.update(item)

    return result['info']


def start_auto(but, token, chat_id):
    option = Option(but)
    item = option.find(token, chat_id)

    if not item:
        item = {'token': token,
                'chat_id': chat_id,
                'auto': 'False',
                'last_call_id': '0'}

    else:
        item = item[0]

    if item['auto'] == 'True':
        return 'Для данного чата звонки уже выгружаются автоматически'

    item['auto'] = 'True'
    option.update(item)
    new_thread(but, token, chat_id)

    return 'Автоматическая выгрузка звонков включена'


def stop_auto(but, token, chat_id):
    option = Option(but)
    item = option.find(token, chat_id)
    if not item:
        return ('Выбранных параметров нет в истории. Проверьте значения'
                '<br>Если хотите добавить значения, то выберите "выгрузка" или "автоматическая выгрузка"')
    item = item[0]
    item['auto'] = 'False'
    option.update(item)

    return 'Автоматическая выгрузка будет остановлена'
