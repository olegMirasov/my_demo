from django.shortcuts import render
from django.http import HttpResponse
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from settings import DOMAIN


APP_PATH = 'my_task_deadline'
SIDEBAR_PATH = 'sidebar/'
WIDGET_PATH = f'https://{DOMAIN}/{APP_PATH}/{SIDEBAR_PATH}'
WORK_PATH = WIDGET_PATH + '-1/'


@main_auth(on_cookies=True)
def update(request):
	return render(request, 'my_deadline_update.html')


@main_auth(on_cookies=True)
def install(request):
	but = request.bitrix_user_token
	PLACEMENT = 'TASK_VIEW_SIDEBAR'
	HANDLER = WORK_PATH
	LANG_ALL = {'ru': {'TITLE': 'Перенос срока задачи на сутки', 'DESCRIPTION': 'Приложение переносит срок сдачи текущего задания на сутки вперед'}}

	props = {'PLACEMENT': PLACEMENT,
			 'HANDLER': HANDLER,
			 'LANG_ALL': LANG_ALL}
	try:
		res = but.call_api_method('placement.bind', props)['result']
	except Exception as ex:
		print(ex)
		return HttpResponse('Вероятно, этот обработчик уже установлен')

	return HttpResponse('install')


@main_auth(on_cookies=True)
def delete(request):
	but = request.bitrix_user_token
	PLACEMENT = 'TASK_VIEW_SIDEBAR'
	HANDLER = WORK_PATH
	props = {'PLACEMENT': PLACEMENT, 'HANDLER': HANDLER}
	try:
		res = but.call_api_method('placement.unbind', props)['result']
	except Exception as ex:
		print(ex)
		return HttpResponse(str(ex))

	return HttpResponse('delete')
