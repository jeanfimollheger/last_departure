from django.contrib import admin
from .models import Project, Task


# Register your models here.
# tasks/admin.py
from django.contrib import admin
from .models import Project, Task

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "creator", "deadline", "private")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("description", "project", "area", "done", "deadline")
    list_filter = ("done", "area", "project")
    prepopulated_fields = {"slug": ("description",)}
