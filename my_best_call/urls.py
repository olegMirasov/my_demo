from django.urls import path
from .views.views import my_search_calls, my_create_task, main_view

urlpatterns = [
    path('', main_view, name="my_main_view"),
    path('search_calls/', my_search_calls, name="my_search_calls"),
    path('create_task/', my_create_task, name="my_create_task"),
]
