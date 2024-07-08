from ..main_class import Command
import json
from random import randint


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
    def answer(cls, bot_id, dialog_id, user_message, user):
        # return {'BOT_ID': bot_id, 'DIALOG_ID': dialog_id, 'MESSAGE': "Сообщение"}
        if not user.status:
            user.status = cls.TAG
            user.save()
            message = ('Это простая игра на угадывания числа от нуля до "выбранного вами"\n'
                       'Для выхода из игры напишите "exit" или "выход"\n\nНапишите верхнюю границу')
            return {'BOT_ID': bot_id, 'DIALOG_ID': dialog_id, 'MESSAGE': message}

        if user_message.lower() in ['exit', 'выход']:
            cls.reset_user(user)
            message = 'Вы вышли из игры'
            return {'BOT_ID': bot_id, 'DIALOG_ID': dialog_id, 'MESSAGE': message}

        data = Helper.from_json(user.data)
        if not data.gaming:
            if not user_message.isdigit():
                message = 'Ваше сообщение не является ни командой, ни числом.\nНапишите целое положительное число'
                return {'BOT_ID': bot_id, 'DIALOG_ID': dialog_id, 'MESSAGE': message}

            data.top_number = int(user_message)
            data.number = randint(0, data.top_number)
            data.gaming = True
            data.count = 0

            new_json = data.get_json()
            user.status = cls.TAG
            user.data = new_json
            user.save()

            message = f'Я загадал число от 0 до {data.top_number}.\nПопробуй угадать)'
            return {'BOT_ID': bot_id, 'DIALOG_ID': dialog_id, 'MESSAGE': message}

        # если пользователь находится в состоянии игры
        if not user_message.isdigit():
            message = 'Ваше сообщение не является ни командой, ни числом.\nНапишите целое положительное число'
            return {'BOT_ID': bot_id, 'DIALOG_ID': dialog_id, 'MESSAGE': message}

        number = int(user_message)
        if number > data.number:
            message = 'Мое число меньше'
            data.count += 1
            user.data = data.get_json()
            user.save()
            return {'BOT_ID': bot_id, 'DIALOG_ID': dialog_id, 'MESSAGE': message}
        elif number < data.number:
            message = 'Мое число больше'
            data.count += 1
            user.data = data.get_json()
            user.save()
            return {'BOT_ID': bot_id, 'DIALOG_ID': dialog_id, 'MESSAGE': message}

        # Если мы дошли до этого момента, то пользовтель угадал число
        message = f'Вы угадали! Это число {data.number}!!!\nСовершено попыток - {data.count + 1}'
        cls.reset_user(user)
        return {'BOT_ID': bot_id, 'DIALOG_ID': dialog_id, 'MESSAGE': message}









