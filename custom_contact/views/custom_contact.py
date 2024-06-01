from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def custom_contact(request):
    """ Отображение контактов на странице """
    but = request.bitrix_user_token
    contacts = but.call_list_method('crm.contact.list')

    # Берем только данные, которые будут отображаться на странице
    # В нашем случае 'ID' 'NAME' 'SECOND_NAME' 'LAST_NAME'
    need_list = ['ID', 'NAME', 'SECOND_NAME', 'LAST_NAME']
    temp_list = []
    for contact in contacts:
        temp_list.append({key: contact[key] for key in need_list})

    temp_dict = {
        'contacts': temp_list,
        'item_list': need_list
    }

    return render(request, 'contact_list.html', temp_dict)
