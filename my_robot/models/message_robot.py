from integration_utils.bitrix_robots.models import BaseRobot
import requests as req
from settings import DOMAIN


class MessageRobot(BaseRobot):
    CODE = 'message_robot'
    NAME = 'Робот пишет случайное сообщение'
    USE_SUBSCRIPTION = True
    USE_PLACEMENT = False
    APP_DOMAIN = DOMAIN

    PROPERTIES = {
        'user': {
            'Name': {'ru': 'Получатель'},
            'Value': {'ru': 'Ответственный'},
            'Type': 'user',
            'Required': 'Y'}
    }

    RETURN_PROPERTIES = {
        'message': {
            'Name': {'ru': 'Сообщение'},
            'Type': 'string',
            'Required': 'Y',
        },
        'ok': {
            'Name': {'ru': 'ok'},
            'Type': 'bool',
            'Required': 'Y',
        },
        'error': {
            'Name': {'ru': 'error'},
            'Type': 'string',
            'Required': 'N',
        },
    }

    def process(self) -> dict:
        try:
            responce = req.get('https://v2.jokeapi.dev/joke/Programming?format=txt')
            text = responce.text
            message = f'Шутка про программирование\n{text}'
            self.dynamic_token.call_api_method('bizproc.event.send', {"event_token": self.event_token,
                                                                      "return_values": {"message": message, 'ok': True}})
            print('skbfaifabusaoh ept')
        except KeyError:
            self.dynamic_token.call_api_method('bizproc.event.send', {"event_token": self.event_token,
                                                                      "return_values": {"message": 'Не удалось получить сообщение',
                                                                                        'ok': False}})

        except Exception as exc:
            return dict(ok=False, error=str(exc))

        return dict(ok=True)
