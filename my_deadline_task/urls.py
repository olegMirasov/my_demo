from django.urls import path
from .views.loads import SIDEBAR_PATH, update, install, delete
from .views.widget import main_view

# my_task_deadline/ - Путь к панели
# my_task_deadline/update/ - Путь к выбору установка.удаление
# my_task_deadline/install/ - Путь к установке
# my_task_deadline/delete/ - Путь к установке

# path('<str:index>/', find_manager, name='my_find_manager'),

urlpatterns = [
    path(SIDEBAR_PATH + '<str:index>/', main_view, name='my_deadline_main'),
    path('update/', update, name='my_deadline_update'),
    path('install/', install, name='my_deadline_install'),
    path('delete/', delete, name='my_deadline_delete'),
]
