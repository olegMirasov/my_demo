from django.shortcuts import render
from django.http import HttpResponse
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from ..notes_bot.bot import Bot
from integration_utils.bitrix24.models.bitrix_user import BitrixUser


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
    bot_props = Bot.get_bot_props()
    bot_code = bot_props['CODE']
    all_bots = but.call_list_method('imbot.bot.list')

    bot_id = None
    for bot in all_bots.values():
        if bot['CODE'] == bot_code:
            bot_id = bot['ID']
            break

    if not bot_id:
        return HttpResponse(f'<h1>ОШИБКА! {bot_props["PROPERTIES"]["NAME"]} не зарегистрирован</h1>')

    try:
        but.call_api_method('imbot.unregister', {'BOT_ID': bot_id})
    except:
        return HttpResponse(f'<h1>Не удалось удалить "{bot_props["PROPERTIES"]["NAME"]}"</h1>')
    return HttpResponse(f'<h1>Бот {bot_props["PROPERTIES"]["NAME"]} удален</h1>')


def main_view(request):
    return render(request, 'bot_load_view.html')


@main_auth(on_start=True)
def work_bot(request):
    but = request.bitrix_user_token
    admin_but = BitrixUser.objects.filter(is_admin=True, user_is_active=True).first().bitrix_user_token
    post = request.POST
    Bot.answer(admin_but, post)
    return HttpResponse('')


