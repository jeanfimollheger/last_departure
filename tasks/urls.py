from django.urls import path
from .views import ProjectListView, ProjectDetailView, ProjectCreateView

urlpatterns = [
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/new/', ProjectCreateView.as_view(), name='project_create'),
    path('projects/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
]