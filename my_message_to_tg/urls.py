from django.urls import path
from .views.views import message_to_tg

urlpatterns = [
    path('', message_to_tg, name='message_to_tg')
]
