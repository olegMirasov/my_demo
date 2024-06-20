
# 7094560822:AAEmuKdm4rrFVDTkxawCTszSqyN--Az8PC8
# 1240601236

from integration_utils.vendors.telegram import Bot


def send_message(token, chat_id, message):
    try:
        bot = Bot(token=token)
        bot.send_message(text=message, chat_id=chat_id)
    except:
        return 'Ошибка. Проверьте токен бота и/или ID чата'

    return 'Сообщение отправлено'
