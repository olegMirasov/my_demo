from django.urls import path

from .views.custom_contact import custom_contact

urlpatterns = [
    path('custom_contact/', custom_contact, name="custom_contact")
]
