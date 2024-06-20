from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from ..utils import send_message


@main_auth(on_cookies=True)
def message_to_tg(request):
    if request.method == 'POST':
        bot_id = request.POST.get('bot_id')
        chat_id = request.POST.get('chat_id')
        message = request.POST.get('message')
        info = send_message(bot_id, chat_id, message)
        context = {'done': True, 'info': info}
        return render(request, 'my_message_to_tg.html', context)
    context = {'done': False, 'info': ''}
    return render(request, 'my_message_to_tg.html', context)
