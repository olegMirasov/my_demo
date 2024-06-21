import threading
import time
from .utils import upload_calls
from .options import Option


SLEEP_TIME = 10  # Через какой промежуток времени будет проверять сообщения


def __running(but, token, chat_id):
    option = Option(but)
    while True:
        item = option.find(token, chat_id)
        if not item:
            return
        item = item[0]
        if item['auto'] == 'False':
            return

        result = upload_calls(but, item)

        if result['change_id']:
            item['last_call_id'] = result['last_id']
            option.update(item)

        time.sleep(SLEEP_TIME)


def new_thread(but, token, chat_id):
    thread = threading.Thread(target=__running, args=(but, token, chat_id))
    thread.start()
    return

