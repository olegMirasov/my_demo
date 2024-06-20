from django import forms


class VoiceToText(forms.Form):
    file = forms.FileField(label='Выберите файл, формат .mp3')
