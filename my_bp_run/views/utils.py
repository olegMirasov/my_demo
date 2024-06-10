from django import forms
import time
import asyncio


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
    start = time.time()
    asyncio.run(_run_process_many(but, bp_id, companies))
    duration = time.time() - start

    return f'Успешно. Процесс запущен по {len(companies)} компаниям. Время выполнения {round(duration)} c.'


async def _run_process_many(but, bp_id, companies):
    temp = []
    for i in companies:
        temp.append(run_one_company(but, bp_id, i['ID']))
    return await asyncio.gather(*temp)


async def run_one_company(but, bp_id, coompany_id):
    return await asyncio.to_thread(but.call_api_method, 'bizproc.workflow.start', {
            'TEMPLATE_ID': bp_id,
            'DOCUMENT_ID': ['crm', 'CCrmDocumentCompany', coompany_id]
        })
