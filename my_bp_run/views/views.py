from django.http import HttpResponse
from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from .utils import *


@main_auth(on_cookies=True)
def my_run_bizproc(request):
    but = request.bitrix_user_token
    # получаем данные для формы
    bp = get_actual_bp(but)
    choices = ((key, key) for key in bp)
    if request.method == 'POST':
        form = get_form(choices)(request.POST)

        if form.is_valid():
            bp_choice = form.cleaned_data['bp']
            bp_id = bp[bp_choice]
            companies_id = but.call_list_method('crm.company.list', {'select': ['ID']})
            message = run_process(but, bp_id, companies_id)
            context = {
                'done': True,
                'message': message,
                'form': get_form(choices)()
            }
            return render(request, 'my_run_bp.html', context)

    form = get_form(choices)()
    context = {
        'done': False,
        'message': '',
        'form': form,
    }
    return render(request, 'my_run_bp.html', context)
