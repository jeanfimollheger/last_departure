from django.urls import path
from .views import ProjectListView, ProjectDetailView, ProjectCreateView, ProjectUpdateView, ProjectDeleteView, TaskCreateView

urlpatterns = [
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/new/', ProjectCreateView.as_view(), name='project_create'),
    path('projects/<slug:slug>/edit/', ProjectUpdateView.as_view(), name='project_update'),
    path('projects/<slug:slug>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    path('projects/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
    path('projects/<slug:project_slug>/tasks/new/', TaskCreateView.as_view(), name='task_create'),
]