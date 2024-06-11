from django.urls import path
from .views.views import my_import_company

urlpatterns = [
    path('', my_import_company, name="my_export_company")
]
