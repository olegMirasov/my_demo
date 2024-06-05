from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from ..forms import CallInfoForm


@main_auth(on_cookies=True)
def reg_call(request):
    but = request.bitrix_user_token
    # 'a23d5b66006e391a006e38f400000001000007dbba8996ade8b0b475aa654b1dac2a82'

    if request.method == 'POST':
        form = CallInfoForm(request.POST, request.FILES)
        if form.is_valid():
            model = form.save()
            model.telephony_externalcall_register(but)
            model.telephony_externalcall_finish(but)
            # model.wav_maker_n_messages(but)
    form = CallInfoForm()
    return render(request, 'my_registercall.html', locals())
