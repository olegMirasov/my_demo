import random
from string import ascii_lowercase


def get_word() -> str:
    """ Возвращает рандомное 'слово' из символов """
    word_len = random.randint(3, 6)
    return ''.join([random.choice(ascii_lowercase) for _ in range(word_len)]).capitalize()


def get_contact_fields() -> dict:
    """ Возвращает рандомные данные для crm.contact.add """
    temp_dict = {
        "NAME": get_word(),
        "SECOND_NAME": get_word(),
        "LAST_NAME": get_word()
    }

    return {"fields": temp_dict}
