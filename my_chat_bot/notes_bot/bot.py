from ..config import BOT_EVENT_HANDLER

INFO = '''Этот бот позволяет сохранять ваши заметки.
/add - Добавить новую
/find - Найти ченибудькакнибудь'''


class Bot:
    # imbot.register
    CODE = 'note_bot'
    TYPE = 'B'
    EVENT_HANDLER = BOT_EVENT_HANDLER
    OPENLINE = 'Y'
    PROPERTIES = {
        'NAME': 'Багаж заметок',
        'COLOR': 'GREEN',
        'WORK_POSITION': 'Сохраняет заметки, анализирует взамосвязи'
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
    def answer(cls, message):
        if message == '/info':
            return INFO
        if message == '/add':
            return 'add some note'
        if message == 'find':
            return 'find some need'
        return 'not avalibl command'
