from settings import DOMAIN

SELF_NAME = 'notes_bot'     # В настройках должен быть указан этот путь
                            # потом можно исправить все через namespace
SELF_PATH = f'https://{DOMAIN}/{SELF_NAME}/'
BOT_INSTALL_PATH = 'install/'
BOT_DELETE_PATH = 'delete/'
BOT_WORK_PATH = 'worker/'

BOT_EVENT_HANDLER = f'{SELF_PATH}{BOT_WORK_PATH}'
