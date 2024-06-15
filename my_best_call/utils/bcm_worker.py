# 1. Определяем необработанные звонки
#     1. запрашиваем в опциях последнюю рабочую дату
#     2. получаем звонки после этой даты, но до текущего дня (не включительно)
#     3. меняем дату
# 2. создаем задачи по необработанным звонка
# 3. сохраняем ид задач
#
#
#
# 1. Определяем выполненные задачи по текущим заданиям
#     1. запрашиваем в опциях ид текущих задач
#     2. выбираем завершенные задачи
#     3. выводим таблицу в чат
# 2. Выводим задачи в чат

import datetime
from prettytable import PrettyTable


call_types = {'1': 'Исходящий', '2': 'Входящий', '3': 'Входящий с перенаправлением', '4': 'Обратный'}


calls_info = {'ID': 'ID звонка',
              'PORTAL_USER_ID': 'ID пользователя',
              'PHONE_NUMBER': 'Номер',
              'CALL_START_DATE': 'Дата',
              'CALL_DURATION': 'Длительность',
              'CALL_TYPE': 'Тип звонка',
              'RECORD_FILE_ID': 'ID файла'}


def _prepare_calls(calls: list[dict], fields: list[str]) -> list[dict]:
    result = []
    for call in calls:
        temp = {}
        for key in fields:
            temp[key] = call[key]
        result.append(temp)
    return result


def get_row(call: dict, fields: list):
    res = []
    for field in fields:
        if call.get(field):
            if field == 'CALL_START_DATE':
                date = datetime.datetime.fromisoformat(call[field])
                date = date.strftime('%d.%m.%Y %H:%M:%S')
                res.append(date)
            elif field == 'CALL_TYPE':
                res.append(call_types[call[field]])
            else:
                res.append(str(call[field]))
        else:
            res.append('NO DATA')

    return res


def create_message(user_calls: dict, fields):

    columns = [calls_info[i] for i in fields]

    messages = dict()
    for user_id, calls in user_calls.items():
        table = PrettyTable()
        table.field_names = columns

        for call in calls:
            table.add_row(get_row(call, fields))

        message = (f"[FONT=monospace]{table}[/FONT]\n\n\nВ качестве результата этой"
                   f" задачи напишите, пожалуйста, ID звонка.\nДля допуска задачи в"
                   f" ленту необходимо выбрать звонок до начала следующего рабочего дня")

        messages[user_id] = message

    return messages


def create_tasks(but, users_messages):
    """ Ставит задачи в сотрудникам в битрикс, возвращает список ID задач """
    result = []
    for user_id, message in users_messages.items():
        task_id = but.call_api_method("tasks.task.add",
                                      {"fields": {
                                          "TITLE": f"Оценить свой лучший звонок",
                                          "CREATED_BY": user_id,
                                          "RESPONSIBLE_ID": user_id,
                                          "DESCRIPTION": message
                                      }})["result"]["task"]["id"]
        result.append((user_id, task_id))
    return result


def get_fio_by_id(but, user_id):
    try:
        user = but.call_list_method('user.get', {"ID": str(user_id)})[0]
        fio = f'{user["LAST_NAME"]} {user["NAME"]}'
    except:
        return 'Данные не найдены'
    return fio


class BCMOptions:
    """ Для работы с опциями приложения на портале Битрикса """
    DATE = 'bcm_date'
    A_TASK = 'bcm_atask'  # актуальные задания
    D_TASK = 'bcm_dtask'  # выполнениые задания
    H_TASK = 'bcm_htask'  # история заданий

    def __init__(self, but):
        self.but = but
        self.date = self.get_date()
        self.a_task = self.get_task(self.A_TASK)
        self.d_task = self.get_task(self.D_TASK)
        self.h_task = self.get_task(self.H_TASK)

    def __get_item(self, key: str):
        result = None
        try:
            result = self.but.call_api_method('app.option.get', {'option': key})['result']
        except Exception as ex:
            print(ex)
            self.__set_item(key)
        return result

    def __set_item(self, key, value=''):
        self.but.call_api_method('app.option.set', {key: value})

    def get_date(self):
        date = self.__get_item(self.DATE)
        if not date:
            date = '2019-08-18T00:00:00+03:00'  # определяем далекую дату
        return datetime.datetime.fromisoformat(date)

    def get_task(self, key: str):
        task = self.__get_item(key)
        if not task:
            task = []
        return task

    def save(self):
        self.__set_item(self.DATE, value=self.date.isoformat())
        self.__set_item(self.A_TASK, value=self.a_task)
        self.__set_item(self.D_TASK, value=self.d_task)
        self.__set_item(self.H_TASK, value=self.h_task)


def prepare_tasks(but):
    # Получаем опции, сравниваем даты. Ищем дату за прошлый день
    options = BCMOptions(but)

    # for debug? delete after
    # options.date = datetime.datetime.fromisoformat('2019-08-18T00:00:00+03:00')
    options.a_task = []
    options.d_task = []
    options.h_task = []


    date_now = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    if options.date.timestamp() >= date_now.timestamp():
        return 'Приложение уже ставило эту задачу. Следующий запуск - завтра', False, []

    calls = but.call_list_method("voximplant.statistic.get",
                                 {"FILTER": {
                                     "<CALL_START_DATE": date_now.isoformat(),
                                     ">=CALL_START_DATE": options.date.isoformat()
                                 }})

    # Достаем только нужную информацию из истории звонков
    fields = ["ID", "PORTAL_USER_ID", "PHONE_NUMBER", "CALL_START_DATE",
              "CALL_DURATION", "CALL_TYPE", "RECORD_FILE_ID"]
    calls = _prepare_calls(calls, fields)

    # Формируем связь сотрудник - звонки
    users_calls = {}
    for call in calls:
        if call.get('PORTAL_USER_ID'):
            user_id = call.get('PORTAL_USER_ID')
            if users_calls.get(user_id):
                users_calls[user_id].append(call)
            else:
                users_calls[user_id] = [call]

    # Формируем сообщения для задания
    show_fields = ["ID", "PHONE_NUMBER", "CALL_START_DATE", "CALL_DURATION", "CALL_TYPE"]
    messages = create_message(users_calls, show_fields)

    # Формируем задания
    users_tasks_id = create_tasks(but, messages)

    # Формируем связь - ID задания и список ID звонков
    new_tasks = []
    for user, task in users_tasks_id:
        calls_arr = users_calls.get(user)
        if not calls_arr:
            new_tasks.append({'task': task, 'calls': []})
            continue
        new_tasks.append({'task': task, 'calls': calls_arr})

    print(new_tasks)

    # Добавляем задания в актуальные в пользовательских опциях
    # Выполненные задания переносим в историю, обновляем дату
    options.a_task = options.a_task + new_tasks
    options.h_task = options.h_task + options.d_task
    options.d_task = []
    options.date = date_now
    options.save()

    # Формируем ответ, который будет отображен на странице
    result = []
    for user_id, task_id in users_tasks_id:
        user_fio = get_fio_by_id(but, user_id)
        count = users_calls.get(user_id)
        if count:
            count = len(count)
        else:
            count = 0
        result.append((user_id, user_fio, count, task_id))

    if result:
        return 'Задачи успешно добавлены', True, result
    return 'За прошлый день звонки не совершались', False, result

