from django.http import HttpResponse
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from ..models.message_robot import MessageRobot


@main_auth(on_cookies=True)
def install(request):
    try:
        MessageRobot.install_or_update('my_robot:my_handler_robot', request.bitrix_user_token)
    except Exception as exc:
        return HttpResponse(str(exc))

    return HttpResponse('ok')
