from integration_utils.bitrix_robots.models import BaseRobot
import requests as req


class MessageRobot(BaseRobot):
    CODE = 'message_robot'
    NAME = 'Робот пишет случайное сообщение'
    USE_SUBSCRIPTION = True
    # USE_PLACEMENT = False
    # PLACEMENT_HANDLER =

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
        print('start ept')
        try:
            '''responce = req.get('https://www.cbr-xml-daily.ru/daily_json.js')
            data = responce.json()
            valute = data['Valute'][self.props['valute']]['Value']'''
            message = 'Test 01 for robot\nOlala'
            self.dynamic_token.call_api_method('bizproc.event.send', {"event_token": self.event_token,
                                                                      "return_values": {"message": message}})
            print('skbfaifabusaoh ept')
        except KeyError:
            self.dynamic_token.call_api_method('bizproc.event.send', {"event_token": self.event_token,
                                                                      "return_values": {"message": 'Не удалось получить сообщение'}})

        except Exception as exc:
            return dict(ok=False, error=str(exc))

        return dict(ok=True)
