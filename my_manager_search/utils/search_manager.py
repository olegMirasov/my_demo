from local_settings import NGROK_URL

LINK = 'my_manager_search/'


def get_user_link(user):
    link = f'{NGROK_URL}/{LINK}{user["ID"]}/'
    text = f'ID: {user["ID"]} | {user["NAME"]} {user["LAST_NAME"]}'
    return link, text


def get_users_list(but):
    users = but.call_list_method('user.get')
    result = []
    for user in users:
        result.append(get_user_link(user))
    return result


def get_users_by_id(but, _id):
    user = but.call_list_method('user.get', {'ID': _id})[0]
    user_link = get_user_link(user)
    user_department = [str(i) for i in user['UF_DEPARTMENT']]
    departments = but.call_list_method('department.get')

    departments_dict = {}
    for element in departments:
        departments_dict.update({element['ID']: element})
        departments_dict[element['ID']].pop('ID')

    result = []
    for i in user_department:
        nach = departments_dict.get(i).get('UF_HEAD')
        if nach == user['ID']:
            order = 1
            parent = departments_dict.get(i).get('PARENT')
            if parent:
                result.append(find_supervisor(departments_dict, parent, order))
        else:
            result.append(find_supervisor(departments_dict, i))

    managers = []
    for manager in result:
        if manager[0] != 'None':
            managers.append(but.call_list_method('user.get', {'ID': manager[0]})[0])

    # подготавливаем данные на возвращение, проверяем есть ли начальники
    if managers:
        manager_links = [get_user_link(manager) for manager in managers]
    else:
        manager_links = [('#', 'Начальники не найдены')]

    return user_link, manager_links


def find_supervisor(departments_dict, current_dep='1', order=0):
    """Рекурсивая функция, осуществляющая поиск начальника, если в настоящем
    подразделении он не был найден."""

    department = departments_dict[current_dep]
    parent_exists = ('PARENT' in department)
    supervisor = department.get('UF_HEAD')
    supervisor_exists = (supervisor and (supervisor != '0'))

    if supervisor_exists:
        return department['UF_HEAD'], order
    else:
        if not parent_exists:
            return "None", order
        return find_supervisor(departments_dict, department['PARENT'], order + 1)


def search_manager(but):
    """Осуществляет поиск начальника для пользователя."""

    users = but.call_list_method('user.get')
    departments = but.call_list_method('department.get')

    #  Записываем в словарь юзеров только поля из массива user_fields и их значения.
    user_fields = ['ID', 'NAME', 'LAST_NAME', 'SECOND_NAME', 'UF_DEPARTMENT']
    user_dict = {}
    for element in users:
        user_dict.update({element['ID']: {}})
        for field in user_fields:
            try:
                user_dict[element['ID']].update({field: element[field]})
            except KeyError:
                pass
        user_dict[element['ID']].pop('ID')

    #  Записываем в словарь подразделения
    departments_dict = {}
    for element in departments:
        departments_dict.update({element['ID']: element})
        departments_dict[element['ID']].pop('ID')

    # Проходимся по всем юзерам, для каждого ищем руководителей.
    for user_id in user_dict:
        user = user_dict[user_id]

        # Руководителей записываем в сет, чтобы не искать дубликаты.
        user.update({'SUPERVISORS': set()})
        for department_id in departments_dict:
            #  Смотрим, состоит ли человек в текущем подразделении.
            #  Если состоит, то в качестве кого?
            if departments_dict[department_id].get('UF_HEAD') == user_id:
                if "PARENT" in departments_dict[department_id]:
                    department = departments_dict[department_id]['PARENT']
                    supervisor_id, order = find_supervisor(departments_dict, department, order=1)
                else:
                    supervisor_id = "None"

            else:
                if int(department_id) in user['UF_DEPARTMENT']:
                    department = department_id
                    supervisor_id, order = find_supervisor(departments_dict, department)
                else:
                    continue
            #  В функцию поиска передается родительское подразделение, если в текущем
            #   юзер является руководителем. В ином случае передается текущее.


            if supervisor_id != "None":
                supervisor = user_dict[supervisor_id]
                conj_str = ""
                for key in ['LAST_NAME', 'NAME', 'SECOND_NAME']:
                    try:
                        conj_str += f'{supervisor[key]} '
                    except KeyError:
                        pass
                conj_str += f"| ID: {supervisor_id} | Порядок: {order}"
                user['SUPERVISORS'].add((supervisor_id, conj_str))
        if user['SUPERVISORS'] == set():
            user['SUPERVISORS'] = ""

    for user_id in user_dict:
        user = user_dict[user_id]
        conj_str = ""
        for key in ['LAST_NAME', 'NAME', 'SECOND_NAME']:
            try:
                conj_str += f"{user[key]} "
            except KeyError:
                pass
        conj_str += f"| ID: {user_id}"
        user.update({'FULL_NAME': conj_str})

    return user_dict, user_fields
