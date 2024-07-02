from django.urls import path
from .views import my_ag_grid

urlpatterns = [
    path('', my_ag_grid, name='my_ag_grid')
]
