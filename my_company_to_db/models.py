from django.db import models
import json


class BitrixCompany(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    data = models.JSONField()

    @staticmethod
    def load_companies(but):
        companies = but.call_list_method('crm.company.list')
        companies = {item['ID']: item for item in companies}

        pre_company = []
        for index, data in companies.items():
            data_json = json.dumps(data, ensure_ascii=False)
            pre_company.append(BitrixCompany(id=index, data=data_json))

        len_comp = len(pre_company)
        if len_comp != 0:
            BitrixCompany.objects.bulk_create(pre_company, update_conflicts=True,
                                              unique_fields=['id'],
                                              update_fields=['data'])
        return f'В базе данных обновлена информация по {len_comp} компаниям'

