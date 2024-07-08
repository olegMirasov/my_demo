import json

class Command:
    TAG = '!write yours tag'
    DESCRIPTION = '!write yours DESCRIPTION'

    @classmethod
    def answer(cls, bot_id, dialog_id, message, user):
        raise ValueError(f'Необходимо переопределить метод "answer" {cls.__name__}')

    @classmethod
    def reset_user(cls, user):
        data = json.dumps({})
        user.data = data
        user.status = ''
        user.save()
