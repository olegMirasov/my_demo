from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

from .utils import prepare_user_info


@main_auth(on_cookies=True)
def select_user(request):
    table = False
    if request.method == 'POST':
        but = request.bitrix_user_token
        user_id = request.POST.get('user_id')
        res = but.call_api_method("user.get", {'ID': user_id})['result'][0]
        res = prepare_user_info(res)
        table = True
    return render(request, 'my_select_user.html', locals())
