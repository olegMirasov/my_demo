import json


class CRM:
    # (field, headerName)
    columns = [
        ('ID', 'АЙДИ')
    ]

    def __init__(self, items: list):
        self.items = items

        self._data = self.get_data()
        self._defs = self.get_defs()

    def get_options(self, option_name):
        s1 = f'const {option_name} = ' + '{\n'
        s2 = f'rowData: {self._data},\n'
        s3 = f'columnDefs: {self._defs}' + '};'
        return s1 + s2 + s3

    def get_data(self):
        new_items = []
        for item in self.items:
            temp = dict()
            for column in self.columns:
                key = column[0]
                temp[key] = item.get(key)
            new_items.append(temp)
        return json.dumps(new_items, ensure_ascii=False)

    def get_defs(self):
        defs = []
        for column in self.columns:
            temp = {
                'field': column[0],
                'headerName': column[1] if column[1] else column[0]
            }
            defs.append(temp)

        return json.dumps(defs, ensure_ascii=False)


class Company(CRM):
    columns = [
        ('TITLE', 'Наименование'),
        ('ADDRESS_CITY', 'Город'),
        ('ADDRESS', 'Адрес'),
    ]


class Lead(CRM):
    columns = [
        ('NAME', 'Имя'),
        ('SECOND_NAME', 'Фамилия'),
        ('LAST_NAME', 'Отчество'),
        ('TITLE', ''),
    ]


class Contact(CRM):
    columns = [
        ('ID', ''),
        ('NAME', 'Имя'),
        ('SECOND_NAME', 'Фамилия'),
        ('LAST_NAME', 'Отчество'),
        ('TYPE_ID', 'Тип'),
    ]


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
