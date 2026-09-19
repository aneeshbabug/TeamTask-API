from django.urls import path
from . import views

urlpatterns = [
path('api/tasks/',views.TaskView.as_view(),name='task-list'),
path('api/tasks/<int:id>/',views.SpecificTaskView.as_view(),name='specific-task'),
path('api/projects/<int:id>/tasks/',views.ProjectSpecificTaskView.as_view(),name='project-task-list'),
]