from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from .models import Task, Project
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProjectForm, TaskForm
from django.urls import reverse_lazy, reverse
class ProjectListView(ListView):
    model = Project
    template_name = 'tasks/project_list.html'
    context_object_name = 'projects'
    #paginate_by = 10

    def get_queryset(self):
        return Project.objects.filter(creator=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        print("\n====== REQUEST ======")
        print("path:", request.path)
        print("method:", request.method)
        print("kwargs:", self.kwargs)
        print("args:", self.args)
        print("GET:", request.GET)
        print("POST:", request.POST)
        print("user:", request.user)
        print("model:", self.model)
        print("user:", request.user.username)
        print("\n=== ALL REQUEST ===")
        for attr in dir(request):
            if not attr.startswith("_"):
                try:
                    value = getattr(request, attr)
                    print(attr, "=>", type(value))
                except Exception as e:
                    print(attr, "=> ERROR:", e)
        print("=====================\n")
        print("=====================\n")
        print("\n======= FIN =_dict_======")
        """
        for k, v in request.__dict__.items():
            print(k, "=>", type(v), v)
        """
        print("=====================\n")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        print("\n====== CONTEXT ======")
        for k, v in context.items():
            print(k, "=>", type(v), v)
        print("=====================\n")

        return context

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
    context_object_name = "project"

    def form_valid(self, form):
        # On impose le créateur
        form.instance.creator = self.request.user
        return super().form_valid(form)
    
class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    #fields = ["name", "deadline", "private"]
    template_name = "tasks/project_form.html"
    form_class = ProjectForm
    context_object_name = "project"

    def get_queryset(self):
        return Project.objects.filter(creator=self.request.user)

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = "tasks/project_confirm_delete.html"
    context_object_name = "project"
    success_url = reverse_lazy("project_list")

    def get_queryset(self):
        return Project.objects.filter(creator=self.request.user)

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    #success_url = reverse_lazy("project_detail")
    
    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, slug=kwargs['project_slug'])
        if self.project.private and self.project.creator != request.user:
            raise PermissionDenied("Project is private.")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.project = self.project
        return super().form_valid(form)
   
    def get_success_url(self):
        # Redirection vers le détail du projet
        return reverse(
            "project_detail",
            kwargs={"slug": self.project.slug}
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = self.project
        return context

class TaskMarkDoneView(LoginRequiredMixin, View):

    def post(self, request, slug):
        task = get_object_or_404(Task, slug=slug)
        project = task.project

        # 🔐 règles de permissions
        if project.private:
            if request.user != project.creator:
                raise PermissionDenied
        else:
            if request.user != project.creator and request.user != task.creator:
                raise PermissionDenied

        task.done = True
        task.save()

        return redirect("project_detail", slug=project.slug)
    
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    context_object_name = "task"

    def get_object(self, queryset=None):
        task = get_object_or_404(Task, slug=self.kwargs["slug"])
        project = task.project

        if project.private:
            if self.request.user != project.creator:
                raise PermissionDenied
        else:
            if (
                self.request.user != project.creator
                and self.request.user != task.creator
            ):
                raise PermissionDenied

        return task

    def get_success_url(self):
        return self.object.project.get_absolute_url()