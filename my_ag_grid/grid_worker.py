import json


class CRM:
    # (field, headerName)
    columns = [
        ('ID', 'АЙДИ')
    ]

    def __init__(self, items: list):
        self._items = []
        for item in items:
            temp = dict()
            for column in self.columns:
                key = column[0]
                temp[key] = item.get(key)
            self._items.append(temp)
        self._data = json.dumps(self._items, ensure_ascii=False)

        self._defs = []
        for column in self.columns:
            temp = {
                'field': column[0],
                'headerName': column[1] if column[1] else column[0]
            }
            self._defs.append(temp)

        self._defs = json.dumps(self._defs, ensure_ascii=False)

    def get_options(self, option_name):
        s1 = f'const {option_name} = ' + '{\n'
        s2 = f'rowData: {self._data},\n'
        s3 = f'columnDefs: {self._defs}' + '};'
        return s1 + s2 + s3


class Company(CRM):
    columns = [
        ('TITLE', 'Наименование'),
        ('ADDRESS_CITY', 'Город'),
        ('ADDRESS', 'Адрес'),
    ]

    def __init__(self, items):
        super().__init__(items)


class Lead(CRM):
    columns = [
        ('NAME', 'Имя'),
        ('SECOND_NAME', 'Фамилия'),
        ('LAST_NAME', 'Отчество'),
        ('TITLE', ''),
    ]

    def __init__(self, items):
        super().__init__(items)


class GridHTML:
    OPTION = 'gridOption'
    GRID_API = '<script src="https://cdn.jsdelivr.net/npm/ag-grid-community/dist/ag-grid-community.min.js"></script>'

    def __init__(self, div_id: str, crm: CRM):
        self.div_id = div_id
        self.crm = crm

    def get_html_block(self):
        return f'<div class="ag-theme-quartz" style="height: 500px" id="{self.div_id}"></div>'

    def get_script_block(self):
        grid_options = self.crm.get_options(self.OPTION)

        selector = f'const eDiv = document.querySelector("#{self.div_id}");'
        api = f'const gridApi = agGrid.createGrid(eDiv, {self.OPTION});'
        self_script = '\n'.join(('<script>', grid_options, selector, api, '</script>'))
        return self.GRID_API + '\n' + self_script

    def get_data_for_template(self):
        data = {
            'html': self.get_html_block(),
            'script': self.get_script_block()
        }
        return data


# leads = [{'ID': '1', 'TITLE': 'Лид 1', 'HONORIFIC': None, 'NAME': 'Влад', 'SECOND_NAME': 'Викторович', 'LAST_NAME': 'Абобусов', 'COMPANY_TITLE': None, 'COMPANY_ID': None, 'CONTACT_ID': None, 'IS_RETURN_CUSTOMER': 'N', 'BIRTHDATE': '', 'SOURCE_ID': 'CALL', 'SOURCE_DESCRIPTION': None, 'STATUS_ID': 'NEW', 'STATUS_DESCRIPTION': None, 'POST': None, 'COMMENTS': None, 'CURRENCY_ID': 'RUB', 'OPPORTUNITY': '0.00', 'IS_MANUAL_OPPORTUNITY': 'N', 'HAS_PHONE': 'N', 'HAS_EMAIL': 'N', 'HAS_IMOL': 'N', 'ASSIGNED_BY_ID': '1', 'CREATED_BY_ID': '1', 'MODIFY_BY_ID': '1', 'DATE_CREATE': '2024-07-02T10:29:18+03:00', 'DATE_MODIFY': '2024-07-02T10:29:18+03:00', 'DATE_CLOSED': '', 'STATUS_SEMANTIC_ID': 'P', 'OPENED': 'Y', 'ORIGINATOR_ID': None, 'ORIGIN_ID': None, 'MOVED_BY_ID': '1', 'MOVED_TIME': '2024-07-02T10:29:18+03:00', 'ADDRESS': None, 'ADDRESS_2': None, 'ADDRESS_CITY': None, 'ADDRESS_POSTAL_CODE': None, 'ADDRESS_REGION': None, 'ADDRESS_PROVINCE': None, 'ADDRESS_COUNTRY': None, 'ADDRESS_COUNTRY_CODE': None, 'ADDRESS_LOC_ADDR_ID': None, 'UTM_SOURCE': None, 'UTM_MEDIUM': None, 'UTM_CAMPAIGN': None, 'UTM_CONTENT': None, 'UTM_TERM': None, 'LAST_ACTIVITY_BY': '1', 'LAST_ACTIVITY_TIME': '2024-07-02T10:29:18+03:00'}, {'ID': '3', 'TITLE': 'Лид 2', 'HONORIFIC': None, 'NAME': 'Влад', 'SECOND_NAME': 'Арнольдович', 'LAST_NAME': 'Кучин', 'COMPANY_TITLE': None, 'COMPANY_ID': None, 'CONTACT_ID': None, 'IS_RETURN_CUSTOMER': 'N', 'BIRTHDATE': '', 'SOURCE_ID': 'CALL', 'SOURCE_DESCRIPTION': None, 'STATUS_ID': 'NEW', 'STATUS_DESCRIPTION': None, 'POST': None, 'COMMENTS': None, 'CURRENCY_ID': 'RUB', 'OPPORTUNITY': '0.00', 'IS_MANUAL_OPPORTUNITY': 'N', 'HAS_PHONE': 'N', 'HAS_EMAIL': 'N', 'HAS_IMOL': 'N', 'ASSIGNED_BY_ID': '1', 'CREATED_BY_ID': '1', 'MODIFY_BY_ID': '1', 'DATE_CREATE': '2024-07-02T10:29:18+03:00', 'DATE_MODIFY': '2024-07-02T10:29:18+03:00', 'DATE_CLOSED': '', 'STATUS_SEMANTIC_ID': 'P', 'OPENED': 'Y', 'ORIGINATOR_ID': None, 'ORIGIN_ID': None, 'MOVED_BY_ID': '1', 'MOVED_TIME': '2024-07-02T10:29:18+03:00', 'ADDRESS': None, 'ADDRESS_2': None, 'ADDRESS_CITY': None, 'ADDRESS_POSTAL_CODE': None, 'ADDRESS_REGION': None, 'ADDRESS_PROVINCE': None, 'ADDRESS_COUNTRY': None, 'ADDRESS_COUNTRY_CODE': None, 'ADDRESS_LOC_ADDR_ID': None, 'UTM_SOURCE': None, 'UTM_MEDIUM': None, 'UTM_CAMPAIGN': None, 'UTM_CONTENT': None, 'UTM_TERM': None, 'LAST_ACTIVITY_BY': '1', 'LAST_ACTIVITY_TIME': '2024-07-02T10:29:18+03:00'}, {'ID': '5', 'TITLE': 'Лид 3', 'HONORIFIC': None, 'NAME': 'Илья', 'SECOND_NAME': 'Тимурович', 'LAST_NAME': 'Ларгус', 'COMPANY_TITLE': None, 'COMPANY_ID': None, 'CONTACT_ID': None, 'IS_RETURN_CUSTOMER': 'N', 'BIRTHDATE': '', 'SOURCE_ID': 'CALL', 'SOURCE_DESCRIPTION': None, 'STATUS_ID': 'NEW', 'STATUS_DESCRIPTION': None, 'POST': None, 'COMMENTS': None, 'CURRENCY_ID': 'RUB', 'OPPORTUNITY': '0.00', 'IS_MANUAL_OPPORTUNITY': 'N', 'HAS_PHONE': 'N', 'HAS_EMAIL': 'N', 'HAS_IMOL': 'N', 'ASSIGNED_BY_ID': '1', 'CREATED_BY_ID': '1', 'MODIFY_BY_ID': '1', 'DATE_CREATE': '2024-07-02T10:29:18+03:00', 'DATE_MODIFY': '2024-07-02T10:29:18+03:00', 'DATE_CLOSED': '', 'STATUS_SEMANTIC_ID': 'P', 'OPENED': 'Y', 'ORIGINATOR_ID': None, 'ORIGIN_ID': None, 'MOVED_BY_ID': '1', 'MOVED_TIME': '2024-07-02T10:29:18+03:00', 'ADDRESS': None, 'ADDRESS_2': None, 'ADDRESS_CITY': None, 'ADDRESS_POSTAL_CODE': None, 'ADDRESS_REGION': None, 'ADDRESS_PROVINCE': None, 'ADDRESS_COUNTRY': None, 'ADDRESS_COUNTRY_CODE': None, 'ADDRESS_LOC_ADDR_ID': None, 'UTM_SOURCE': None, 'UTM_MEDIUM': None, 'UTM_CAMPAIGN': None, 'UTM_CONTENT': None, 'UTM_TERM': None, 'LAST_ACTIVITY_BY': '1', 'LAST_ACTIVITY_TIME': '2024-07-02T10:29:18+03:00'}, {'ID': '7', 'TITLE': 'Лид 4', 'HONORIFIC': None, 'NAME': 'Тимур', 'SECOND_NAME': 'Ильич', 'LAST_NAME': 'Коргин', 'COMPANY_TITLE': None, 'COMPANY_ID': None, 'CONTACT_ID': None, 'IS_RETURN_CUSTOMER': 'N', 'BIRTHDATE': '', 'SOURCE_ID': 'CALL', 'SOURCE_DESCRIPTION': None, 'STATUS_ID': 'NEW', 'STATUS_DESCRIPTION': None, 'POST': None, 'COMMENTS': None, 'CURRENCY_ID': 'RUB', 'OPPORTUNITY': '0.00', 'IS_MANUAL_OPPORTUNITY': 'N', 'HAS_PHONE': 'N', 'HAS_EMAIL': 'N', 'HAS_IMOL': 'N', 'ASSIGNED_BY_ID': '1', 'CREATED_BY_ID': '1', 'MODIFY_BY_ID': '1', 'DATE_CREATE': '2024-07-02T10:29:18+03:00', 'DATE_MODIFY': '2024-07-02T10:29:18+03:00', 'DATE_CLOSED': '', 'STATUS_SEMANTIC_ID': 'P', 'OPENED': 'Y', 'ORIGINATOR_ID': None, 'ORIGIN_ID': None, 'MOVED_BY_ID': '1', 'MOVED_TIME': '2024-07-02T10:29:18+03:00', 'ADDRESS': None, 'ADDRESS_2': None, 'ADDRESS_CITY': None, 'ADDRESS_POSTAL_CODE': None, 'ADDRESS_REGION': None, 'ADDRESS_PROVINCE': None, 'ADDRESS_COUNTRY': None, 'ADDRESS_COUNTRY_CODE': None, 'ADDRESS_LOC_ADDR_ID': None, 'UTM_SOURCE': None, 'UTM_MEDIUM': None, 'UTM_CAMPAIGN': None, 'UTM_CONTENT': None, 'UTM_TERM': None, 'LAST_ACTIVITY_BY': '1', 'LAST_ACTIVITY_TIME': '2024-07-02T10:29:18+03:00'}, {'ID': '9', 'TITLE': 'Лид 5', 'HONORIFIC': None, 'NAME': 'Николай', 'SECOND_NAME': 'Александрович', 'LAST_NAME': 'Недовес', 'COMPANY_TITLE': None, 'COMPANY_ID': None, 'CONTACT_ID': None, 'IS_RETURN_CUSTOMER': 'N', 'BIRTHDATE': '', 'SOURCE_ID': 'CALL', 'SOURCE_DESCRIPTION': None, 'STATUS_ID': 'NEW', 'STATUS_DESCRIPTION': None, 'POST': None, 'COMMENTS': None, 'CURRENCY_ID': 'RUB', 'OPPORTUNITY': '0.00', 'IS_MANUAL_OPPORTUNITY': 'N', 'HAS_PHONE': 'N', 'HAS_EMAIL': 'N', 'HAS_IMOL': 'N', 'ASSIGNED_BY_ID': '1', 'CREATED_BY_ID': '1', 'MODIFY_BY_ID': '1', 'DATE_CREATE': '2024-07-02T10:29:18+03:00', 'DATE_MODIFY': '2024-07-02T10:29:18+03:00', 'DATE_CLOSED': '', 'STATUS_SEMANTIC_ID': 'P', 'OPENED': 'Y', 'ORIGINATOR_ID': None, 'ORIGIN_ID': None, 'MOVED_BY_ID': '1', 'MOVED_TIME': '2024-07-02T10:29:18+03:00', 'ADDRESS': None, 'ADDRESS_2': None, 'ADDRESS_CITY': None, 'ADDRESS_POSTAL_CODE': None, 'ADDRESS_REGION': None, 'ADDRESS_PROVINCE': None, 'ADDRESS_COUNTRY': None, 'ADDRESS_COUNTRY_CODE': None, 'ADDRESS_LOC_ADDR_ID': None, 'UTM_SOURCE': None, 'UTM_MEDIUM': None, 'UTM_CAMPAIGN': None, 'UTM_CONTENT': None, 'UTM_TERM': None, 'LAST_ACTIVITY_BY': '1', 'LAST_ACTIVITY_TIME': '2024-07-02T10:29:18+03:00'}, {'ID': '11', 'TITLE': 'Лид 6', 'HONORIFIC': None, 'NAME': 'Даниил', 'SECOND_NAME': 'Эдуардович', 'LAST_NAME': 'Розмин', 'COMPANY_TITLE': None, 'COMPANY_ID': None, 'CONTACT_ID': None, 'IS_RETURN_CUSTOMER': 'N', 'BIRTHDATE': '', 'SOURCE_ID': 'CALL', 'SOURCE_DESCRIPTION': None, 'STATUS_ID': 'NEW', 'STATUS_DESCRIPTION': None, 'POST': None, 'COMMENTS': None, 'CURRENCY_ID': 'RUB', 'OPPORTUNITY': '0.00', 'IS_MANUAL_OPPORTUNITY': 'N', 'HAS_PHONE': 'N', 'HAS_EMAIL': 'N', 'HAS_IMOL': 'N', 'ASSIGNED_BY_ID': '1', 'CREATED_BY_ID': '1', 'MODIFY_BY_ID': '1', 'DATE_CREATE': '2024-07-02T10:29:18+03:00', 'DATE_MODIFY': '2024-07-02T10:29:18+03:00', 'DATE_CLOSED': '', 'STATUS_SEMANTIC_ID': 'P', 'OPENED': 'Y', 'ORIGINATOR_ID': None, 'ORIGIN_ID': None, 'MOVED_BY_ID': '1', 'MOVED_TIME': '2024-07-02T10:29:18+03:00', 'ADDRESS': None, 'ADDRESS_2': None, 'ADDRESS_CITY': None, 'ADDRESS_POSTAL_CODE': None, 'ADDRESS_REGION': None, 'ADDRESS_PROVINCE': None, 'ADDRESS_COUNTRY': None, 'ADDRESS_COUNTRY_CODE': None, 'ADDRESS_LOC_ADDR_ID': None, 'UTM_SOURCE': None, 'UTM_MEDIUM': None, 'UTM_CAMPAIGN': None, 'UTM_CONTENT': None, 'UTM_TERM': None, 'LAST_ACTIVITY_BY': '1', 'LAST_ACTIVITY_TIME': '2024-07-02T10:29:18+03:00'}, {'ID': '13', 'TITLE': 'Лид 7', 'HONORIFIC': None, 'NAME': 'Антон', 'SECOND_NAME': 'Роальдович', 'LAST_NAME': 'Мел', 'COMPANY_TITLE': None, 'COMPANY_ID': None, 'CONTACT_ID': None, 'IS_RETURN_CUSTOMER': 'N', 'BIRTHDATE': '', 'SOURCE_ID': 'CALL', 'SOURCE_DESCRIPTION': None, 'STATUS_ID': 'NEW', 'STATUS_DESCRIPTION': None, 'POST': None, 'COMMENTS': None, 'CURRENCY_ID': 'RUB', 'OPPORTUNITY': '0.00', 'IS_MANUAL_OPPORTUNITY': 'N', 'HAS_PHONE': 'N', 'HAS_EMAIL': 'N', 'HAS_IMOL': 'N', 'ASSIGNED_BY_ID': '1', 'CREATED_BY_ID': '1', 'MODIFY_BY_ID': '1', 'DATE_CREATE': '2024-07-02T10:29:18+03:00', 'DATE_MODIFY': '2024-07-02T10:29:18+03:00', 'DATE_CLOSED': '', 'STATUS_SEMANTIC_ID': 'P', 'OPENED': 'Y', 'ORIGINATOR_ID': None, 'ORIGIN_ID': None, 'MOVED_BY_ID': '1', 'MOVED_TIME': '2024-07-02T10:29:18+03:00', 'ADDRESS': None, 'ADDRESS_2': None, 'ADDRESS_CITY': None, 'ADDRESS_POSTAL_CODE': None, 'ADDRESS_REGION': None, 'ADDRESS_PROVINCE': None, 'ADDRESS_COUNTRY': None, 'ADDRESS_COUNTRY_CODE': None, 'ADDRESS_LOC_ADDR_ID': None, 'UTM_SOURCE': None, 'UTM_MEDIUM': None, 'UTM_CAMPAIGN': None, 'UTM_CONTENT': None, 'UTM_TERM': None, 'LAST_ACTIVITY_BY': '1', 'LAST_ACTIVITY_TIME': '2024-07-02T10:29:18+03:00'}, {'ID': '15', 'TITLE': 'Лид 8', 'HONORIFIC': None, 'NAME': 'Александр', 'SECOND_NAME': 'Кузьмич', 'LAST_NAME': 'Мизин', 'COMPANY_TITLE': None, 'COMPANY_ID': None, 'CONTACT_ID': None, 'IS_RETURN_CUSTOMER': 'N', 'BIRTHDATE': '', 'SOURCE_ID': 'CALL', 'SOURCE_DESCRIPTION': None, 'STATUS_ID': 'NEW', 'STATUS_DESCRIPTION': None, 'POST': None, 'COMMENTS': None, 'CURRENCY_ID': 'RUB', 'OPPORTUNITY': '0.00', 'IS_MANUAL_OPPORTUNITY': 'N', 'HAS_PHONE': 'N', 'HAS_EMAIL': 'N', 'HAS_IMOL': 'N', 'ASSIGNED_BY_ID': '1', 'CREATED_BY_ID': '1', 'MODIFY_BY_ID': '1', 'DATE_CREATE': '2024-07-02T10:29:19+03:00', 'DATE_MODIFY': '2024-07-02T10:29:19+03:00', 'DATE_CLOSED': '', 'STATUS_SEMANTIC_ID': 'P', 'OPENED': 'Y', 'ORIGINATOR_ID': None, 'ORIGIN_ID': None, 'MOVED_BY_ID': '1', 'MOVED_TIME': '2024-07-02T10:29:19+03:00', 'ADDRESS': None, 'ADDRESS_2': None, 'ADDRESS_CITY': None, 'ADDRESS_POSTAL_CODE': None, 'ADDRESS_REGION': None, 'ADDRESS_PROVINCE': None, 'ADDRESS_COUNTRY': None, 'ADDRESS_COUNTRY_CODE': None, 'ADDRESS_LOC_ADDR_ID': None, 'UTM_SOURCE': None, 'UTM_MEDIUM': None, 'UTM_CAMPAIGN': None, 'UTM_CONTENT': None, 'UTM_TERM': None, 'LAST_ACTIVITY_BY': '1', 'LAST_ACTIVITY_TIME': '2024-07-02T10:29:19+03:00'}, {'ID': '17', 'TITLE': 'Лид 9', 'HONORIFIC': None, 'NAME': 'Роман', 'SECOND_NAME': 'Вадимович', 'LAST_NAME': 'Кругов', 'COMPANY_TITLE': None, 'COMPANY_ID': None, 'CONTACT_ID': None, 'IS_RETURN_CUSTOMER': 'N', 'BIRTHDATE': '', 'SOURCE_ID': 'CALL', 'SOURCE_DESCRIPTION': None, 'STATUS_ID': 'NEW', 'STATUS_DESCRIPTION': None, 'POST': None, 'COMMENTS': None, 'CURRENCY_ID': 'RUB', 'OPPORTUNITY': '0.00', 'IS_MANUAL_OPPORTUNITY': 'N', 'HAS_PHONE': 'N', 'HAS_EMAIL': 'N', 'HAS_IMOL': 'N', 'ASSIGNED_BY_ID': '1', 'CREATED_BY_ID': '1', 'MODIFY_BY_ID': '1', 'DATE_CREATE': '2024-07-02T10:29:19+03:00', 'DATE_MODIFY': '2024-07-02T10:29:19+03:00', 'DATE_CLOSED': '', 'STATUS_SEMANTIC_ID': 'P', 'OPENED': 'Y', 'ORIGINATOR_ID': None, 'ORIGIN_ID': None, 'MOVED_BY_ID': '1', 'MOVED_TIME': '2024-07-02T10:29:19+03:00', 'ADDRESS': None, 'ADDRESS_2': None, 'ADDRESS_CITY': None, 'ADDRESS_POSTAL_CODE': None, 'ADDRESS_REGION': None, 'ADDRESS_PROVINCE': None, 'ADDRESS_COUNTRY': None, 'ADDRESS_COUNTRY_CODE': None, 'ADDRESS_LOC_ADDR_ID': None, 'UTM_SOURCE': None, 'UTM_MEDIUM': None, 'UTM_CAMPAIGN': None, 'UTM_CONTENT': None, 'UTM_TERM': None, 'LAST_ACTIVITY_BY': '1', 'LAST_ACTIVITY_TIME': '2024-07-02T10:29:19+03:00'}]

