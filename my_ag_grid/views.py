from django.shortcuts import render
from django.http import HttpResponse
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from .utils import get_data_for_choice, get_form, get_data_for_template


@main_auth(on_cookies=True)
def my_ag_grid(request):
    but = request.bitrix_user_token
    choices = get_data_for_choice()
    if request.method == 'POST':
        form = get_form(choices)(request.POST)
        if form.is_valid():
            choice = form.cleaned_data.get('choice')
            data = get_data_for_template(but, choice)

    choices = get_data_for_choice()
    form = get_form(choices)
    return render(request, 'crm_ag_grid.html', locals())
