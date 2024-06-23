from django.urls import path
from .views.views import my_robot
from .views.uninstall import uninstall
from .views.install import install
from .models.message_robot import MessageRobot

app_name = 'my_robot'

urlpatterns = [
    path('', my_robot, name='my_robot'),
    path('install/', install, name='my_robot_install'),
    path('uninstall/', uninstall, name='my_robot_uninstall'),
    path('handler/', MessageRobot.as_view(), name='my_handler_robot'),
]
