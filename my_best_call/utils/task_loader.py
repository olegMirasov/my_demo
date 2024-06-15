from .bcm_worker import BCMOptions
import settings
import html
from datetime import datetime


def parse_date(date_str):
    """Позволяет распарсить дату в удобочитаемом формате"""

    date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    formatted_date = date_obj.strftime("%d %b %Y, %H:%M:%S")

    return formatted_date


def get_call_type(call):
    """Позволяет распарсить тип звонка и вернуть пользователя описание типа
    звонка в строчном формате"""

    call_types = {
        '1': 'Исходящий',
        '2': 'Входящий',
        '3': 'Входящий с перенаправлением',
        '4': 'Обратный звонок',
    }

    return call_types[call]


def get_html_row(call):
    row = f"""<tr>
                        <td>    {call['ID']}  </td>
                        <td>    {call['PHONE_NUMBER']}  </td>
                        <td><a href='https://{settings.APP_SETTINGS.portal_domain}/disk/downloadFile/{call['RECORD_FILE_ID']}/'>Скачать</a></td>
                        <td>    {call['CALL_DURATION']} секунд  </td>
                        <td>    {parse_date(call['CALL_START_DATE'])}  </td>
                        <td>    {get_call_type(call['CALL_TYPE'])}  </td>
                    </tr>\n"""
    return row


def get_html_table(rows):
    html_table = f"""<table>
                        <tr>
                            <th>ID звонка</th>
                            <th>Номер</th>
                            <th>Запись звонка</th>
                            <th>Длительность</th>
                            <th>Дата</th>
                            <th>Тип</th>
                        </tr>
                        {rows}
                    </table>"""
    return html_table


def _get_index_by_id(arr: list, _id):
    for i in range(len(arr)):
        temp_id = arr[i]['id']
        if _id == temp_id:
            return i
    raise ValueError('В списке нет указанного ID')


def _find_call_by_id(arr: list, call_id):
    for call in arr:
        temp_id = call['ID']
        if temp_id == call_id:
            return call
    raise ValueError('В списке нет указанного ID')


def screen_task(but):
    options = BCMOptions(but)

    actual_id = options.a_task
    print(actual_id)

    tasks = []
    for task_item in actual_id:
        task_id = task_item['task']
        temp = but.call_list_method('tasks.task.get', {'taskId': task_id, 'select': ['*']})
        tasks.append(temp['task'])

    # Определяем выполненные и невыполненные задачи
    done, not_done = [], []
    for task in tasks:
        if task['status'] == '5':
            done.append(task)
        else:
            not_done.append(task)

    # Формируем словарь для удобства работы
    actual_dict = dict()
    for item in actual_id:
        key = item['task']
        value = item['calls']
        actual_dict[key] = value

    # Получаем результаты задач
    true_calls = []
    bad_results = []
    for task in done:
        task_res = but.call_api_method("tasks.task.result.list", {"taskId": task["id"]})["result"]
        print(task_res)
        if not task_res:
            but.call_api_method("tasks.task.renew", {"taskId": task["id"]})
            but.call_api_method("task.commentitem.add", {
                "TASKID": task["id"],
                "FIELDS": {
                    "AUTHOR_ID": task["createdBy"],
                    "POST_MESSAGE": "Оставьте комментарий помеченный как результат"
                }
            })
            bad_results.append(task)
            continue

        task_res = task_res[0]['text']
        calls_id = [i["ID"] for i in actual_dict.get(task['id'])]
        if task_res not in calls_id:
            but.call_api_method("tasks.task.renew", {"taskId": task["id"]})
            but.call_api_method("task.commentitem.add", {
                "TASKID": task["id"],
                "FIELDS": {
                    "AUTHOR_ID": task["createdBy"],
                    "POST_MESSAGE": "Как результат укажите ID одного звонка"
                }
            })
            bad_results.append(task)

        true_calls.append(task_res)

    if bad_results:
        for item in bad_results:
            index = _get_index_by_id(done, item['id'])
            not_done.append(done[index])
            done.remove([done[index]])

    # Записываем завершенные и не завершенные задания в опции
    options.h_task.extend(options.d_task)
    options.d_task = done
    options.a_task = []

    options.save()

    # --- создаем сообщение в чат ---
    # получаем группу
    try:
        group_id = but.call_api_method("sonet_group.get", {"FILTER": {"NAME": "Лучший звонок за день"}})["result"][0]["ID"]
    except:
        group_id = but.call_api_method("sonet_group.create", {"NAME": "Лучший звонок за день",
                                                              "VISIBLE": "Y", "OPENED": "Y"})["result"]

    # Получаем необходимые звонки
    app_calls = but.call_list_method("voximplant.statistic.get", {
        "filter": {"ID": true_calls},
        "select": ["ID", "PHONE_NUMBER", "CALL_DURATION", "RECORD_FILE_ID",
                   "CALL_START_DATE", "CALL_TYPE"]
    })

    # формируем сообщение

    rows = ""
    for app_call in app_calls:
        row = get_html_row(app_call)
        rows += row

    html_table = get_html_table(rows)


    but.call_list_method("log.blogpost.add",
                         {"POST_TITLE": f"Новые лучшие звонки",
                          "POST_MESSAGE": f"{html.unescape(html_table)}",
                          "DEST": [f"SG{group_id}"]})

    return 'Если вы видите это сообщение, то обратитесь к разработчикам. Страница не готова', True, []
