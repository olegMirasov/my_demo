import json


class Command:
    TAG = '!write yours tag'
    DESCRIPTION = '!write yours DESCRIPTION'

    @classmethod
    def answer(cls,but, bot_id, dialog_id, user_message, user, message_id, *args, **kwargs):
        raise ValueError(f'Необходимо переопределить метод "answer" {cls.__name__}')

    @classmethod
    def reset_user(cls, user):
        data = json.dumps({'status': 'None'})
        user.data = data
        user.status = ''
        user.save()
