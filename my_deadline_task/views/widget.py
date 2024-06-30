from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from .loads import WIDGET_PATH
from ..utils import parse_task_id, move_task, admin_token, self_task


KEYS = {'to_server': 'На сервере',
        'to_admin': 'С токеном админа',
        'to_self': 'Только свои'}

FUNCS = {'to_server': lambda *args: move_task(*args),
         'to_admin': lambda *args: admin_token(*args),
         'to_self': lambda *args: self_task(*args)}


items = [(WIDGET_PATH + k + '/', v) for k, v in KEYS.items()]


@main_auth(on_cookies=True)
def main_view(request, index):
    task_id = request.POST.get('PLACEMENT_OPTIONS')
    if task_id:
        task_id = parse_task_id(task_id)
    else:
        task_id = request.GET.get('taskId')

    user_id = str(request.bitrix_user.bitrix_id)

    but = request.bitrix_user_token
    info = 'Выберите необходимое действие'
    if index in FUNCS.keys():
        # Порядок должен быть такой (but, task_id, user_id)
        info = FUNCS[index](but, task_id, user_id)

    context = {'taskId': task_id, 'items': items, 'info': info}

    return render(request, 'widget.html', context)
