import requests
from integration_utils.vendors.telegram import Bot

call_types = {
        '1': 'Исходящий',
        '2': 'Входящий',
        '3': 'Входящий с перенаправлением',
        '4': 'Обратный звонок',
    }


def get_calls(but, last_id):
    calls = but.call_list_method('voximplant.statistic.get', {'FILTER': {'>ID': last_id}, 'SORT': 'ID'})

    return calls


def get_fio_by_id(but, user_id):
    try:
        user = but.call_list_method('user.get', {"ID": str(user_id)})[0]
        fio = f'{user["LAST_NAME"]} {user["NAME"]}'
    except:
        return 'Данные не найдены'
    return fio


def get_file(but, file_id):
    if not file_id:
        return

    file_info = but.call_api_method('disk.file.get', {'id': file_id})['result']
    url = file_info.get('DOWNLOAD_URL')

    response = requests.get(url)
    return file_info.get('NAME'), response.content


def upload_calls(but, item: dict) -> dict:
    calls = get_calls(but, item['last_call_id'])
    if not calls:
        result = {'info': 'Новых звонков не обнаружено',
                  'change_id': False,
                  'last_id': '0'}

        return result

    bot = Bot(token=item.get('token'))
    chat_id = item.get('chat_id')

    for call in calls:
        user = get_fio_by_id(but, call.get('PORTAL_USER_ID'))
        number = call.get('PHONE_NUMBER')
        call_type = call_types[call.get('CALL_TYPE')]

        message = '\n'.join([user, number, call_type])

        file_id = call.get('RECORD_FILE_ID')
        file_name, file = get_file(but, file_id)
        if not file:
            bot.send_message(chat_id=chat_id, text=f'{message}\nФайл звонка не загружен')
            continue

        bot.send_audio(chat_id=chat_id, audio=file, caption=message, filename=file_name)

    last_id = calls[-1]['ID']

    result = {'info': 'Звонки успешно выгружены',
              'change_id': True,
              'last_id': last_id}

    return result
