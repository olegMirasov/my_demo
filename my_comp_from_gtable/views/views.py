from django.http import HttpResponse
from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from .utils import *
from ..forms import GTable


# url = 'https://docs.google.com/spreadsheets/d/1ZuKXEK0hwJyxFwGxoi77G0PaOh4Qg4SDZBNkHDws2iU/edit#gid=1891471437'


@main_auth(on_cookies=True)
def my_import_company(request):
    but = request.bitrix_user_token
    context = {'done': True, 'info': [('--Не удалось', 'Проверьте ссылку, правильность таблицы')]}
    if request.method == 'GET':
        form = GTable()
        context = {'done': False, 'form': form}
    elif request.method == 'POST':
        form = GTable(request.POST)
        if form.is_valid():
            link = form.cleaned_data['link']
            item_list = get_data_by_link(link, prepare=True)  # Получаем наименования сущностей и их поля
            info = B24Loader.add_to_bitrix(but, item_list)

            context = {'done': True, 'info': info}

    return render(request, 'company_from_gtable.html', context)
