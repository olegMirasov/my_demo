from django.urls import path
from .views.views import call_to_telegram

urlpatterns = [
    path('', call_to_telegram, name='my_call_to_telegram')
]
