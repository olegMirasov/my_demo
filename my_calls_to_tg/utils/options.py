GROUP_NAME = 'CallTg_'  # Ключ в опциях. Значения - список из словарей по типу как ниже

example = {'token': 'Токен бота',
           'chat_id': 'ID чата',
           'auto': 'Выгружаются ли звонки (True, False)',
           'last_call_id': 'ID последнего выгруженного звонка'}


class Option:
    def __init__(self, but, group: str | None = None):
        self.but = but
        if group:
            self.group = group
        else:
            self.group = GROUP_NAME
        self.__check_option()

    def __check_option(self):
        res = self.but.call_api_method('app.option.get', {'option': self.group})['result']
        if not res:
            self.but.call_api_method('app.option.set', {self.group: None})

    def find(self, token: str | None = None, chat_id: str | None = None) -> list:
        items = self.but.call_list_method('app.option.get', {'option': self.group})
        if not items:
            return []

        if not token and not chat_id:
            return items

        if token and not chat_id:
            result = []
            for item in items:
                if item['token'] == token:
                    result.append(item)
            return result

        if chat_id and not token:
            result = []
            for item in items:
                if item['chat_id'] == chat_id:
                    result.append(item)
            return result

        result = []
        for item in items:
            if item['token'] == token and item['chat_id'] == chat_id:
                result.append(item)
        return result

    def update(self, u_item: dict):
        token = u_item['token']
        chat_id = u_item['chat_id']

        items = self.but.call_list_method('app.option.get', {'option': self.group})
        if not items:
            items = [u_item]
            self.but.call_api_method('app.option.set', {self.group: items})

        flag = False
        for item in items:
            if item['token'] == token and item['chat_id'] == chat_id:
                flag = True
                item['auto'] = u_item['auto']
                item['last_call_id'] = u_item['last_call_id']
                break

        if not flag:
            items.append(u_item)

        self.but.call_api_method('app.option.set', {self.group: items})






