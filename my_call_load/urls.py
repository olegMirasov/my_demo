from django.urls import path

from .views import my_reg_call

urlpatterns = [
    path('my_call/', my_reg_call, name="my_reg_call")
]
