from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from .models import BitrixCompany


@main_auth(on_cookies=True)
def company_to_db(request):
    if request.method == 'POST':
        but = request.bitrix_user_token
        info = BitrixCompany.load_companies(but)

        context = {'info': info}
        return render(request, 'my_comp_to_db.html', context)
    context = {'info': ''}
    return render(request, 'my_comp_to_db.html', context)
