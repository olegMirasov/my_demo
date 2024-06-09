from django.urls import path
from .views.views import upload_excel

urlpatterns = [
    path('', upload_excel, name="my_upload_excel")
]
