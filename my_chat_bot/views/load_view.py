from django.shortcuts import render
from django.http import HttpResponse
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from ..notes_bot.bot import Bot

@main_auth(on_cookies=True)
def load_bot(request):
    but = request.bitrix_user_token
    bot_props = Bot.get_bot_props()
    try:
        but.call_api_method('imbot.register', bot_props)
    except:
        return HttpResponse(f'<h1>Бот {bot_props["PROPERTIES"]["NAME"]} уже установлен</h1>')
    return HttpResponse(f'<h1>Install {bot_props["PROPERTIES"]["NAME"]}</h1>')


@main_auth(on_cookies=True)
def delete_bot(request):
    but = request.bitrix_user_token
    return HttpResponse(f'<h1>Delete {but}</h1>')


def main_view(request):
    return render(request, 'bot_load_view.html')


@main_auth(on_start=True)
def work_bot(request):
    but = request.bitrix_user_token
    post = request.POST
    Bot.answer(but, post)
    return HttpResponse('')


