from ..main_class import Command
from .keyboard import KEYBOARD
from .config import NUMBERS, RED, BLACK, COLOR_DICT, COM_EXIT, COM_COIN, COINS

import random
import json


VALUES = [str(i) for i in NUMBERS] + [RED, BLACK]


class Helper:
    def __init__(self, gaming=False, coins=None, price=None, origin_message_id=None, *args, **kwargs):
        self.gaming = gaming
        self.coins = coins if coins else 100
        self.price = price if price else COINS[0]
        self.origin_message_id = origin_message_id

    def get_json(self):
        temp = {
            'gaming': self.gaming,
            'coins': self.coins,
            'price': self.price,
            'origin_message_id': self.origin_message_id
        }
        return json.dumps(temp, ensure_ascii=False)

    @classmethod
    def from_json(cls, data):
        temp = json.loads(data)
        return Helper(**temp)


class Casino(Command):
    TAG = '/casino'
    DESCRIPTION = 'Простая игра в рулетку (Казино)'

    @classmethod
    def answer(cls, but, bot_id, dialog_id, user_message, user, message_id, *args, **kwargs):

        if not user.status:
            data = Helper()
            data.gaming = True

            message = f"Добро пожаловать в игру!\nНа вашем счете {data.coins} монет, первоначальная ставка {data.price} монет"
            origin_message_id = but.call_api_method('imbot.message.add', {'BOT_ID': bot_id, 'DIALOG_ID': dialog_id,
                                                                          'MESSAGE': message, 'KEYBOARD': KEYBOARD})
            print(origin_message_id)
            data.origin_message_id = origin_message_id['result']
            print(data.origin_message_id)

            user.status = cls.TAG
            user.data = data.get_json()
            user.save()
            return None

        data = Helper.from_json(user.data)

        if user_message == COM_EXIT:
            cls.reset_user(user)
            cls.delete_self_message(but, bot_id, data)

            message = f"Вы вышли из игры. Ваш счет: {data.coins} монет"
            return {'BOT_ID': bot_id, 'DIALOG_ID': dialog_id, 'MESSAGE': message}

        if user_message.startswith(COM_COIN):

            price = user_message.lstrip(COM_COIN)
            if not price.isdigit():
                message = 'Количество монет должно быть цифрой'
            else:
                data.price = int(price)
                message = f'Ваша ставка {data.price} монет\nКошелек: {data.coins}'

            cls.update_self_message(but, bot_id, data, user, dialog_id, message)
            return

        # сама игра
        if user_message not in VALUES:
            message = 'Неопознаная команда'
            cls.update_self_message(but, bot_id, data, user, dialog_id, message)
            return

        if data.price > data.coins:
            message = (f'Ваша ставка слишком велика\n'
                       f'Ставка: {data.price}\nКошелек: {data.coins}')
            cls.update_self_message(but, bot_id, data, user, dialog_id, message)
            return

        win_number = str(random.choice(NUMBERS))
        if user_message in [RED, BLACK]:
            color = COLOR_DICT[win_number]
            if color == user_message:
                cls.win(data, 2)
                message = f'Выпало число {win_number}\nВыйгрыш. Кошелек: {data.coins}\nСтавка: {data.price}'
            else:
                cls.lose(data)
                message = f'Выпало число {win_number}\nПроигрыш. Кошелек: {data.coins}\nСтавка: {data.price}'

            cls.update_self_message(but, bot_id, data, user, dialog_id, message)
            return

        if user_message == win_number:
            cls.win(data, len(NUMBERS))
            message = f'Выпало число {win_number}\nВыйгрыш. Кошелек: {data.coins}\nСтавка: {data.price}'
        else:
            cls.lose(data)
            message = f'Выпало число {win_number}\nПроигрыш. Кошелек: {data.coins}\nСтавка: {data.price}'

        cls.update_self_message(but, bot_id, data, user, dialog_id, message)

    @staticmethod
    def win(data, step):
        win = data.price * step
        data.coins += win - data.price

    @staticmethod
    def lose(data, step=0):
        data.coins -= data.price

    @classmethod
    def update_self_message(cls, but, bot_id, data, user, dialog_id, message):
        cls.delete_self_message(but, bot_id, data)
        arr = {'BOT_ID': bot_id, 'DIALOG_ID': dialog_id, 'MESSAGE': message, 'KEYBOARD': KEYBOARD}
        origin_message_id = but.call_api_method('imbot.message.add',
                                                arr)['result']
        data.origin_message_id = origin_message_id

        user.data = data.get_json()
        user.save()

    @classmethod
    def delete_self_message(cls, but, bot_id, data: Helper):
        but.call_api_method('imbot.message.delete', {'BOT_ID': bot_id, 'MESSAGE_ID': data.origin_message_id, 'COMPLETE': 'Y'})


