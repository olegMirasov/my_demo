from django.urls import path
from .views.find_manager import find_manager


urlpatterns = [
    path('<str:index>/', find_manager, name='my_find_manager'),
]
