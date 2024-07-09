from ..config import BOT_EVENT_HANDLER
from ..models import ChatBotControl
from .command_register import REGISTER
from .commands.info.info import Info


COMMANDS = {use_command.TAG: use_command for use_command in REGISTER}

# Создаем актуальные описания для команды информации
INFO_COMMAND = Info.TAG
Info.create_descriptions(REGISTER)


KEYBOARD = {
        'TEXT': f'{Info.TAG}',
        'ACTION': 'SEND',
        'ACTION_VALUE': f'{Info.TAG}',
        'DISPLAY': 'LINE',
        'BG_COLOR': '#02f70b',
        'TEXT_COLOR': '#111'
    }


class Bot:
    # imbot.register
    CODE = 'my_some_bot'
    TYPE = 'S'
    EVENT_HANDLER = BOT_EVENT_HANDLER
    OPENLINE = 'Y'
    PROPERTIES = {
        'NAME': 'Игробот',
        'COLOR': 'GREEN',
        'WORK_POSITION': 'Делу - время, потехе - "Игробот"'
    }

    @classmethod
    def get_bot_props(cls):
        props = {
           'CODE': cls.CODE,
           'TYPE': cls.TYPE,
           'OPENLINE': cls.OPENLINE,
           'EVENT_HANDLER': cls.EVENT_HANDLER,
           'PROPERTIES': cls.PROPERTIES,
        }
        return props

    @classmethod
    def answer(cls, but, post):
        '''for k, v in post.items():
            print(k, v)'''

        # Получаем необходимые данные
        bot_id = post.get('data[PARAMS][TO_USER_ID]')
        dialog_id = post.get('data[PARAMS][DIALOG_ID]')
        message = post.get('data[PARAMS][MESSAGE]')
        user_id = post.get('data[USER][ID]')
        message_id = post.get('data[PARAMS][MESSAGE_ID]')

        # Узнаем, есть ли у пользователя текущая сессия в одном из обработчиков
        user = ChatBotControl.objects.get_or_create(pk=user_id)[0]
        print(user)

        if user.status:
            command = COMMANDS.get(user.status)
        else:
            command = COMMANDS.get(message)

        if not command:
            answer = f'Данной команды не найдено. Попробуйте отправить команду "{INFO_COMMAND}" для получения информации'
            but.call_api_method('imbot.message.add', {'BOT_ID': bot_id, 'DIALOG_ID': dialog_id,
                                                      'MESSAGE': answer, 'KEYBOARD': [KEYBOARD]})
            return

        answer = command.answer(but=but,
                                bot_id=bot_id,
                                dialog_id=dialog_id,
                                user_message=message,
                                user=user,
                                message_id=message_id)
        if answer and type(answer) is dict:
            but.call_api_method('imbot.message.add', answer)
