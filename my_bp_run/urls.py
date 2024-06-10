from django.urls import path
from .views.views import my_run_bizproc

urlpatterns = [
    path('', my_run_bizproc, name='my_run_bizproc'),
]
