from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('todo-list',views.TodoList,name="todo-list"),
    path('search-autocompletion',views.search_autocompletion,name="search_autocompletion"),
    path('task-create',views.TaskCreateView.as_view(),name="task_create"),
    path('task-update/<str:pk>/',views.TaskUpdateView.as_view(),name="task_update"),
    path('task-delete/<str:pk>/',views.deleteTask,name="task_delete"),
    path('send-email',views.send_email,name="send_email")
]
