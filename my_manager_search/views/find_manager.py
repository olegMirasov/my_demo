from django.shortcuts import render, HttpResponse
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from ..utils.search_manager import *


@main_auth(on_cookies=True)
def find_manager(request, index):
    but = request.bitrix_user_token
    if index == '-1':
        users = get_users_list(but)
        context = {'users': users, 'all': f'{NGROK_URL}/{LINK}all/'}
        return render(request, 'users.html', context)
    if index == 'all':
        user_dict, user_fields = search_manager(but)
        return render(request, 'list.html', context={'fields': user_fields, 'users': user_dict})
    user, managers = get_users_by_id(but, index)
    context = {'user': [user], 'managers': managers}
    return render(request, 'one_user.html', context)
