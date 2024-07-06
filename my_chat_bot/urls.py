from django.urls import path
from .views.load_view import load_bot, delete_bot, main_view, work_bot
from .config import *

urlpatterns = [
    path('', main_view, name='my_bot_main_view'),
    path(BOT_INSTALL_PATH, load_bot, name='my_load_bot'),
    path(BOT_DELETE_PATH, delete_bot, name='my_delete_bot'),
    path(BOT_WORK_PATH, work_bot, name='my_work_bot'),
]
