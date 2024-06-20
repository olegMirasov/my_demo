from django.urls import path
from .views.views import my_open_ai

urlpatterns = [
    path('', my_open_ai, name='my_open_ai'),
]
