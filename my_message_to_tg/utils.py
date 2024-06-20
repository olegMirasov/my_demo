

from integration_utils.vendors.telegram import Bot


def send_message(token, chat_id, message):
    try:
        bot = Bot(token=token)
        bot.send_message(text=message, chat_id=chat_id)
    except:
        return 'Ошибка. Проверьте токен бота и/или ID чата'

    return 'Сообщение отправлено'
