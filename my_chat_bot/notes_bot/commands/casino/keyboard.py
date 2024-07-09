from .config import *


class Color:
    RED = '#f70202'
    GREEN = '#02f70b'
    BLACK = '#171717'

    def __init__(self):
        self.count = -1

    def get(self):
        self.count += 1
        if self.count == 0:
            return self.GREEN

        if self.count % 2 == 0:
            color = self.RED
        else:
            color = self.BLACK
        return color


colors = Color()
num_buttons = []
for num in NUMBERS:
    title = str(num)
    temp = {
        'TEXT': f'_{title}_',
        'ACTION': 'SEND',
        'ACTION_VALUE': title,
        'DISPLAY': 'LINE',
        'BG_COLOR': colors.get(),
        'TEXT_COLOR': '#fff'
    }
    num_buttons.append(temp)

num_buttons.append({'TYPE': 'NEWLINE'})

num_buttons.append({'TEXT': 'Черное',
                    'ACTION': 'SEND',
                    'ACTION_VALUE': BLACK,
                    'DISPLAY': 'LINE',
                    'BG_COLOR': colors.BLACK,
                    'TEXT_COLOR': '#fff'},)

num_buttons.append({'TEXT': 'Красное',
                    'ACTION': 'SEND',
                    'ACTION_VALUE': RED,
                    'DISPLAY': 'LINE',
                    'BG_COLOR': colors.RED,
                    'TEXT_COLOR': '#fff'})

num_buttons.append({'TYPE': 'NEWLINE'})

for coin in COINS:
    value = str(coin)
    temp = {
        'TEXT': value,
        'ACTION': 'SEND',
        'ACTION_VALUE': COM_COIN + value,
        'DISPLAY': 'LINE',
        'BG_COLOR': '#111213',
        'TEXT_COLOR': '#fff'
    }
    num_buttons.append(temp)

num_buttons.append({'TYPE': 'NEWLINE'})

num_buttons.append({'TEXT': 'Выход',
                    'ACTION': 'SEND',
                    'ACTION_VALUE': COM_EXIT,
                    'DISPLAY': 'LINE',
                    'BG_COLOR': colors.GREEN})

KEYBOARD = num_buttons

'''ACTION – действие, может быть одно из следующих типов (REST ревизии 28):
PUT – вставить в поле ввода.
SEND – отправить текст.
COPY – копировать текст в буфер обмена.
CALL – позвонить.
DIALOG – открыть указанный диалог.
ACTION_VALUE – значение, для каждого типа означает свое (REST ревизии 28):
PUT – текст, который будет вставлен в поле ввода.
SEND – текст, который будет отправлен.
COPY – текст, который будет скопирован в буфер обмена.
CALL – номер телефона в международном формате.
DIALOG – идентификатор диалога, это может быть ID пользователя, либо ID чата в формате chatXXX.'''
