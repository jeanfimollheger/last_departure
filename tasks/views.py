from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Task, Project
from django.contrib.auth.mixins import LoginRequiredMixin

class ProjectListView(ListView):
    model = Project
    template_name = 'project_list.html'
    context_object_name = 'projects'
    #paginate_by = 10

    def get_queryset(self):
        return Project.objects.filter(creator=self.request.user)
    
class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'project_detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        return Project.objects.filter(creator=self.request.user)