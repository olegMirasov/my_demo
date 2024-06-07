from django import forms
from .views.help_utils import get_data_for_choice


class ChoiceForm(forms.Form):
    choice = forms.ChoiceField(choices=get_data_for_choice(), label='Выберите необходимую crm сущность')
