from django import forms


class MessageToTg(forms.Form):
    bot_token = forms.CharField(label='Токен бота')
    chat_id = forms.CharField(label='ID чата')
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 20}))
