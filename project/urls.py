from django.urls import path
from . import views

urlpatterns = [
    path('api/projects/', views.ProjectListCreateView.as_view(),name='project-list'),
    path('api/projects/<int:id>/', views.ProjectDetailView.as_view(),name='project-detail'),
    path('api/projects/<int:id>/members/', views.ProjectMemberListCreateView.as_view(),name='project-members'),
    path('api/projects/<int:id>/members/<int:mem_id>/', views.ProjectMemberDetailView.as_view(),name='project-member-detail'),
]