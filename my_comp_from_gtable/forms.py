from django import forms


class GTable(forms.Form):
    link = forms.CharField(label='Ссылка')

