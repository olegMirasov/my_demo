from django.urls import path

from .views.find_duplicate import find_duplicate

urlpatterns = [
    path('', find_duplicate, name='my_find_duplicate'),
]
