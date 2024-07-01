from datetime import datetime

USAGE_FIELDS = ['ID', 'NAME', 'LAST_NAME', 'EMAIL', 'DATE_REGISTER', 'PERSONAL_PHOTO']


def _bt_date(date):
    temp = datetime.fromisoformat(date)
    bt_date = temp.strftime('%d.%m.%Y')
    return bt_date


def prepare_user_info(user_data):
    res = {}
    for key in USAGE_FIELDS:
        res[key] = user_data.get(key)
        if key == 'DATE_REGISTER':
            res[key] = _bt_date(user_data.get(key))
    return res
