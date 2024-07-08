from ..main_class import Command


class Info(Command):
    TAG = '/info'
    DESCRIPTION = 'Выводит информацию по поддерживаемым командам'
    __text = ''

    @classmethod
    def answer(cls, bot_id, dialog_id, answer, user):
        return {'BOT_ID': bot_id, 'DIALOG_ID': dialog_id, 'MESSAGE': cls.__text}

    @classmethod
    def create_descriptions(cls, commands: list):
        temp = ['Поддерживаемые команды:\n'] + [f'{c.TAG} - {c.DESCRIPTION}' for c in commands]
        cls.__text = '\n'.join(temp)