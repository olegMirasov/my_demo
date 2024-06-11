from django.db import models
from settings import MEDIA_URL
from mutagen.mp3 import MP3
import os
import base64


class NumberChoicesType(models.IntegerChoices):
    one = 1, 'Исходящий'
    two = 2, 'Входящий'
    three = 3, 'Входящий с перенаправлением'
    four = 4, 'Обратный'


class NumberChoicesAddToChat(models.IntegerChoices):
    zero = 0, 'Не уведомлять'
    one = 1, 'Уведомлять'


class CallInfo(models.Model):
    user_phone = models.CharField(max_length=20, null=False, blank=False)
    user_id = models.IntegerField(blank=False, null=False)
    phone_number = models.CharField(max_length=50, blank=False, null=False)
    call_date = models.DateTimeField(blank=True, null=True)
    type = models.IntegerField(null=False, blank=False,
                               choices=NumberChoicesType.choices)
    duration = models.IntegerField(null=True, blank=True)
    add_to_chat = models.IntegerField(blank=True, null=True,
                                      choices=NumberChoicesAddToChat.choices)
    call_id = models.CharField(max_length=255, null=True, blank=True)

    inner_media_path = "rings/"
    filename = ""
    file = models.FileField(upload_to=inner_media_path, null=True, blank=True)
    # messages = models.TextField(blank=True, null=True)

    def telephony_externalcall_register(self, but):

        res = but.call_api_method("telephony.externalcall.register", {
            "USER_PHONE_INNER": self.user_phone,
            "USER_ID": self.user_id,
            "PHONE_NUMBER": self.phone_number,
            "CALL_START_DATE": self.call_date,
            "TYPE": self.type
        })

        self.call_id = res['result']['CALL_ID']
        self.duration = 0
        if self.file:
            self.duration = int(MP3(self.file).info.length)
        self.filename = str(self.file)[len(self.inner_media_path):-len(os.path.splitext(str(self.file))[-1])]

        self.save()

    def telephony_externalcall_finish(self, but):
        but.call_api_method('telephony.externalcall.finish', {
            "CALL_ID": self.call_id,
            "USER_ID": self.user_id,
            "DURATION": self.duration,
            "ADD_TO_CHAT": self.add_to_chat,
        })

    def telephony_externalcall_attach_record(self, but):
        with open(MEDIA_URL[1:] + self.file.name, 'rb') as file:
            ring = file.read()

        try:
            but.call_api_method('telephony.externalCall.attachRecord', {
                "CALL_ID": self.call_id,
                "FILENAME": self.file.name,
                "FILE_CONTENT": base64.b64encode(ring),
            })
        except Exception as ex:
            print('Не удалось загрузить звонок')
            print(ex)


