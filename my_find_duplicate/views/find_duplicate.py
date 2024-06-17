
from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from .help_utils import get_duplicate

from ..forms import ChoiceForm


@main_auth(on_cookies=True)
def find_duplicate(request):
    but = request.bitrix_user_token

    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            field = form.cleaned_data['choice']                 # получаем выбранную сущность
            duplicates = get_duplicate(but=but, field=field)    # получаем дубликаты

            context = {
                'field': field,
                'data': duplicates
            }
            return render(request, 'show_duplicates.html', context)

    form = ChoiceForm()

    return render(request, 'my_sort_fields.html', locals())

