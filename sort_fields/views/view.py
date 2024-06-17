from django.shortcuts import render
from django.http import HttpResponse
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from .utils import *


@main_auth(on_cookies=True)
def sort_field(request):
    but = request.bitrix_user_token
    user_fields = but.call_list_method('crm.company.userfield.list')
    choices = get_choices(user_fields)

    if request.method == 'POST':
        form = get_form(choices)(request.POST)

        if form.is_valid():
            field_id = form.cleaned_data['id']
            info = do_sort(but, field_id)
        else:
            info = 'Произошла ошибка. Пожалуйста, проверьте свои данные'

        context = {'done': True, 'form': form, 'info': info}
        return render(request, 'my_sort_fields.html', context)

    form = get_form(choices)()
    context = {'done': False, 'form': form, 'info': 'Вы можете посмотреть путь поля в строке браузера'}
    return render(request, 'my_sort_fields.html', context)
