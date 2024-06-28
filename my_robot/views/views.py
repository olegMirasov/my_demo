from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def my_robot(request):
    return render(request, 'my_robot.html')
