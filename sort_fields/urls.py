from django.urls import path

from .views.view import sort_field

urlpatterns = [
    path('', sort_field, name="my_sort_field")
]
