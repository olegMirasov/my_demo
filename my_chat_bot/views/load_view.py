from django.shortcuts import render
from django.http import HttpResponse
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from ..notes_bot.bot import Bot

@main_auth(on_cookies=True)
def load_bot(request):
    but = request.bitrix_user_token
    bot_props = Bot.get_bot_props()
    print(bot_props)
    bot_id = but.call_api_method('imbot.register', bot_props)
    print(bot_id)
    return HttpResponse(f'<h1>Install {but}</h1>')


@main_auth(on_cookies=True)
def delete_bot(request):
    but = request.bitrix_user_token
    return HttpResponse(f'<h1>Delete {but}</h1>')


def main_view(request):
    return render(request, 'bot_load_view.html')


@main_auth(on_start=True)
def work_bot(request):
    but = request.bitrix_user_token
    z = request.POST
    b_id = z.get('data[BOT][13][BOT_ID]')
    c_id = z.get('data[PARAMS][DIALOG_ID]')
    mes = z.get('data[PARAMS][MESSAGE]')
    answer = Bot.answer(mes)
    but.call_api_method('imbot.message.add', {'BOT_ID': b_id,'DIALOG_ID': c_id, 'MESSAGE': answer})
    return HttpResponse('')


