from django.shortcuts import render
from django.http import FileResponse
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from .utils import ProductManager


@main_auth(on_cookies=True)
def upload_excel(request):
    but = request.bitrix_user_token
    worker = ProductManager(but)
    if request.method == 'POST':
        form = worker.get_form()(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            path = worker.save_and_get_path(code)
            file = open(path, 'rb')
            response = FileResponse(file)

            response['Content-Disposition'] = 'attachment; filename="example.xlsx"'
            return response

    form = worker.get_form()()
    context = {'form': form}
    return render(request, 'upload_excel_prod.html', context)
