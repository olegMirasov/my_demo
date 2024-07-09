from ..main_class import Command


class Info(Command):
    TAG = '/info'
    DESCRIPTION = 'Выводит информацию по поддерживаемым командам'
    __text = ''
    KEYBOARD = None

    _keyboard_hor_count = 3

    @classmethod
    def answer(cls, but, bot_id, dialog_id, user_message, user, *args, **kwargs):
        if not cls.KEYBOARD:
            return {'BOT_ID': bot_id, 'DIALOG_ID': dialog_id, 'MESSAGE': cls.__text}
        return {'BOT_ID': bot_id, 'DIALOG_ID': dialog_id, 'MESSAGE': cls.__text, 'KEYBOARD': cls.KEYBOARD}

    @classmethod
    def create_descriptions(cls, commands: list):
        temp = ['Поддерживаемые команды:\n'] + [f'{c.TAG} - {c.DESCRIPTION}' for c in commands]
        cls.__text = '\n'.join(temp)

        # create keyboard
        keyboard = []
        count = 0
        for item in commands:
            temp = {
                    'TEXT': f'{item.TAG}',
                    'ACTION': 'SEND',
                    'ACTION_VALUE': f'{item.TAG}',
                    'DISPLAY': 'LINE',
                    'BG_COLOR': '#02f70b',
                    'TEXT_COLOR': '#111'}
            keyboard.append(temp)
            count += 1

            if count >= cls._keyboard_hor_count:
                count = 0
                keyboard.append({'TYPE': 'NEWLINE'})

        cls.KEYBOARD = keyboard


