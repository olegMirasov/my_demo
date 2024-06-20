import time

from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from ..forms import VoiceToText
from openai import OpenAI
from settings import OPEN_AI_API_KEY, BASE_DIR


@main_auth(on_cookies=True)
def my_open_ai(request):

    if request.method == 'POST':
        form = VoiceToText(request.POST, request.FILES)
        if form.is_valid():
            bin_file = form.cleaned_data['file'].read()
            try:
                client = OpenAI(api_key=OPEN_AI_API_KEY)
                transcript = client.audio.translations.create(file=bin_file, model='whisper-1')
                text = transcript.text
                context = {
                    'done': True,
                    'info': 'Текст преобразован. Не забудьте скопировать результат',
                    'text': text
                }
            except:
                context = {
                    'done': True,
                    'info': 'Текст НЕ преобразован.',
                    'text': ' Сервис OpenAI не предоставляет свои услуги в вашей стране.'
                }
        else:
            context = {
                'done': True,
                'info': 'Что-то пошло не так. Попробуйте позднее',
                'text': ''
            }

        return render(request, 'voice_to_text.html', context)

    form = VoiceToText()
    context = {
        'done': False,
        'form': form,
        'info': 'Преобразование в текст может занять некоторое время'
    }
    return render(request, 'voice_to_text.html', context)
