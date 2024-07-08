from django.db import models
import json


class ChatBotControl(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)  # user id in bitrix
    status = models.CharField(default='')  # status для текущей сессии, пустой статус - сессия отсутствует

    def_json = json.dumps({})
    data = models.JSONField(default=def_json)  # данные для текущей сессии

    def __str__(self):
        return f'user {self.id}. status: {self.status}'
