from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Task, Project
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProjectForm

class ProjectListView(ListView):
    model = Project
    template_name = 'tasks/project_list.html'
    context_object_name = 'projects'
    #paginate_by = 10

    def get_queryset(self):
        return Project.objects.filter(creator=self.request.user)
    
class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'tasks/project_detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        return Project.objects.filter(creator=self.request.user)
    
class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    #fields = ["name", "deadline", "private"]
    template_name = "tasks/project_form.html"
    form_class = ProjectForm

    def form_valid(self, form):
        # On impose le créateur
        form.instance.creator = self.request.user
        return super().form_valid(form)
