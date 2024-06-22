from django.http import HttpResponseForbidden, JsonResponse

from integration_utils.bitrix24.models import BitrixUser
from integration_utils.its_utils.app_get_params import get_params_from_sources


@get_params_from_sources
def export_deals(request):
    """
    Функция отвечает за сбор данных из битрикса, обработку в нужный вид и
    отправку в PowerBI.
    """
    # https://apparently-endless-wren.ngrok-free.app/deal_for_powerbi/export_deals/?key=DoiyHseg8yuJBChuibaKa

    if request.its_params.get('key') != 'DoiyHseg8yuJBChuibaKa':
        return HttpResponseForbidden()
    but = BitrixUser.objects.filter(is_admin=True,
                                    user_is_active=True).first().bitrix_user_token

    deals = but.call_list_method('crm.deal.list',
                                 {'select': ['ASSIGNED_BY_ID', 'COMPANY_ID', 'CONTACT_IDS', 'DATE_CREATE', 'TITLE']})

    companies = but.call_list_method('crm.company.list',
                                     {'select': ['ADDRESS', 'ADDRESS_CITY', 'ID', 'LEAD_ID', 'TITLE']})

    contacts = but.call_list_method('crm.contact.list',
                                    {'select': ['ID', 'LEAD_ID', 'NAME', 'LAST_NAME', 'COMPANY_IDS']})

    leads = but.call_list_method('crm.lead.list',
                                 {'select': ["ID", "TITLE", "STATUS_ID", "OPPORTUNITY", "CURRENCY_ID"]})

    result = {
        'deals': deals,
        'companies': companies,
        'contacts': contacts,
        'leads': leads
    }

    return JsonResponse(result, safe=False)
