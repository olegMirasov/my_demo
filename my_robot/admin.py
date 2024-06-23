from django.contrib import admin

from .models.message_robot import MessageRobot
from integration_utils.itsolution.functions.auto_register import auto_register

auto_register('robot_currency')

admin.site.register(MessageRobot)
