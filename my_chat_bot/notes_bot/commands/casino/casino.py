from ..main_class import Command


class Casino(Command):
    TAG = '/casino'
    DESCRIPTION = 'Простая игра в рулетку (Казино)'

    @classmethod
    def answer(cls, bot_id, dialog_id, answer, user):
        return {'BOT_ID': bot_id, 'DIALOG_ID': dialog_id, 'MESSAGE': "casino worker"}