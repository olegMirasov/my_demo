from local_settings import NGROK_URL

LINK = 'my_manager_search/'



def get_users_list(but):
    users = but.call_list_method('user.get')
    result = []
    for user in users:
        link = f'{NGROK_URL}/{LINK}{user["ID"]}/'
        text = f'ID: {user["ID"]} | {user["NAME"]} {user["LAST_NAME"]}'
        result.append((link, text))
    return result
