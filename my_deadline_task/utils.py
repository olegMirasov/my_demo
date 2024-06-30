import datetime as dt
from integration_utils.bitrix24.models.bitrix_user import BitrixUser


def parse_task_id(item: str):
    items = item.split('"taskId":"')[-1]
    items = items.split('"')[0]
    return items


def move_task(but, task_id, *args):
    task = but.call_api_method('tasks.task.get', {'taskId': task_id, 'fields': ["DEADLINE"]})['result']['task']
    print(task)
    task_deadline = dt.datetime.fromisoformat(task['deadline'])
    new_deadline = task_deadline + dt.timedelta(days=1)
    new_deadline = dt.datetime.isoformat(new_deadline)
    but.call_api_method('tasks.task.update', {'taskId': task_id, 'fields': {"DEADLINE": new_deadline}})
    return 'Задача передвинута'


def admin_token(but, task_id, *args):
    admin_but = BitrixUser.objects.filter(is_admin=True, user_is_active=True).first().bitrix_user_token
    return move_task(admin_but, task_id)


def self_task(but, task_id, user_id):
    task = but.call_api_method('tasks.task.get', {'taskId': task_id, 'fields': ["CREATED_BY "]})['result']['task']
    user = task['createdBy']
    if user != user_id:
        return 'Можно двигать только свои задачи!'
    return move_task(but, task_id)
