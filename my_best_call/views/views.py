from django.http import HttpResponse
from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from ..utils.bcm_worker import prepare_tasks
from ..utils.task_loader import screen_task


@main_auth(on_cookies=True)
def my_search_calls(request):
    but = request.bitrix_user_token
    result = screen_task(but)
    return render(request, 'bcm_main_view.html')


@main_auth(on_cookies=True)
def my_create_task(request):
    but = request.bitrix_user_token
    result = prepare_tasks(but)
    context = {'message': result[0], 'flag': result[1], 'items': result[-1]}
    return render(request, 'bcm_create_task.html', context)


def main_view(request):
    return render(request, 'bcm_main_view.html')
