from ..main_class import Command
import json


class Helper:
    def __init__(self, gaming=False, top_number=None, number=None, count=None, *args, **kwargs):
        self.gaming = gaming
        self.top_number = top_number if top_number else 1000
        self.number = number if number else 123
        self.count = count if count else 0

    def get_json(self):
        temp = {
            'gaming': self.gaming,
            'top_number': self.top_number,
            'number': self.number,
            'count': self.count
        }
        return json.dumps(temp, ensure_ascii=False)

    @classmethod
    def from_json(cls, data):
        temp = json.loads(data)
        return Helper(**temp)


class Number(Command):
    TAG = '/find_number'
    DESCRIPTION = 'Игра - угадай число'

    @classmethod
    def answer(cls, bot_id, dialog_id, message, user):
        # return {'BOT_ID': bot_id, 'DIALOG_ID': dialog_id, 'MESSAGE': "Сообщение"}
        if not user.status:
            message = ('Это простая игра на угадывания числа от нуля до "выбранного вами"\n'
                       'Для выхода из игры напишите "exit" или "выход"\n\nНапишите верхнюю границу')
            return {'BOT_ID': bot_id, 'DIALOG_ID': dialog_id, 'MESSAGE': message}

        if message.lower() in ['exit', 'выход']:
            cls.reset_user(user)
            message = 'Вы вышли из игры'
            return {'BOT_ID': bot_id, 'DIALOG_ID': dialog_id, 'MESSAGE': message}

        data = Helper.from_json(user.data)
        if not data.gaming:
            message = 'Это простая игра на угадывания числа от нуля до "выбранного вами"\n\nНапишите верхнюю границу'
            return {'BOT_ID': bot_id, 'DIALOG_ID': dialog_id, 'MESSAGE': message}



