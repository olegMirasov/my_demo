from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from ..utils.call_worker import add_all, start_auto, stop_auto


DO = {'all': lambda but, token, chat_id: add_all(but, token, chat_id),
      'start': lambda but, token, chat_id: start_auto(but, token, chat_id),
      'stop': lambda but, token, chat_id: stop_auto(but, token, chat_id)}


@main_auth(on_cookies=True)
def call_to_telegram(request):
    if request.method == 'POST':
        but = request.bitrix_user_token

        bot_token = request.POST['bot_token']
        chat_id = request.POST['chat_id']
        choice = request.POST['choice']
        info = DO[choice](but, bot_token, chat_id)

        context = {'info': info}
        return render(request, 'my_call_to_telegram.html', context)

    context = {'run_flag': False}
    return render(request, 'my_call_to_telegram.html', context)
