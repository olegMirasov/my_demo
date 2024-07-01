from django.urls import path
from .views import select_user

urlpatterns = [
    path('', select_user, name='my_select_user')
]
