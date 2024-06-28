from django.urls import path
from .views.views import main_view, update, install, delete
from .views.views import SIDEBAR_PATH

# my_task_deadline/ - Путь к панели
# my_task_deadline/update/ - Путь к выбору установка.удаление
# my_task_deadline/install/ - Путь к установке
# my_task_deadline/delete/ - Путь к установке


urlpatterns = [
    path(SIDEBAR_PATH, main_view, name='my_deadline_main'),
    path('update/', update, name='my_deadline_update'),
    path('install/', install, name='my_deadline_install'),
    path('delete/', delete, name='my_deadline_delete'),
]
