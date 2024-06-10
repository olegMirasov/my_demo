from django import forms


crm_fields = {'Лиды': 'crm.lead.list',
              'Компании': 'crm.company.list',
              'Контакты': 'crm.contact.list',
              'Товары': 'crm.product.property.list'}


def get_actual_crm(*args):
    pass


def get_actual_bp(but, crm='company'):
    res_bizprocs = but.call_list_method('bizproc.workflow.template.list',
                                        {'select': ["ID", "NAME"],
                                         'filter': {"DOCUMENT_TYPE": [
                                             "crm",
                                             f"CCrmDocument{crm.capitalize()}",
                                             f"{crm.upper()}"
                                         ]}})
    return {item['NAME']: item['ID'] for item in res_bizprocs}


def get_form(choices):
    class ChoiceForm(forms.Form):
        bp = forms.ChoiceField(choices=choices,
                               label='Выберите бизнес процесс')
    return ChoiceForm


def run_process(but, bp_id, companies):
    for company in companies:
        but.call_api_method('bizproc.workflow.start', {
            'TEMPLATE_ID': bp_id,
            'DOCUMENT_ID': ['crm', 'CCrmDocumentCompany', str(company['ID'])]
        })

    return f'Успешно. Процесс запущен по {len(companies)} компаниям'
