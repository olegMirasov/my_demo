from django import forms
from .grid_worker import *


crm_classes = {'Лиды': Lead,
               'Компании': Company,
               'Контакты': CRM,
               'Товары': CRM}


crm_commands = {'Лиды': 'crm.lead.list',
                'Компании': 'crm.company.list',
                'Контакты': 'crm.contact.list',
                'Товары': 'crm.product.property.list'}


def get_data_for_template(but, choice):
    crm_list = get_crm_list(but, name=choice)
    crm_ent = crm_classes.get(choice)(crm_list)

    worker = GridHTML(div_id='myGridCrm', crm=crm_ent)
    return worker.get_data_for_template()


def get_crm_list(but, name):
    result = but.call_list_method(crm_commands.get(name))
    print(name)
    print(result)
    return result


def get_data_for_choice():
    return ((key,  key) for key in crm_commands.keys())


def get_form(choices):
    class ChoiceCRM(forms.Form):
        choice = forms.ChoiceField(choices=choices, label='CRM')

    return ChoiceCRM
