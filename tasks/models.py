from django.db import models
from django.conf import settings
from django.utils.text import slugify

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects"
    )
    slug = models.SlugField(unique=True, blank=True)
    deadline = models.DateField(blank=True, null=True)
    private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['deadline', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Task(models.Model):
    AREA_CHOICES = [
        ('Fin', 'Finance'),
        ('RH', 'Ressources Humaines'),
        ('Org', 'Organisation'),
        ('Dev', 'Code'),
        ('Bud', 'Budget'),
        ('Perso', 'Personnel'),
        ('SRIA', 'SRIA Tools'),        
    ]
    description = models.CharField(max_length=255)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    deadline = models.DateField(blank=True, null=True)
    done = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)
    area = models.CharField(max_length=20, choices=AREA_CHOICES, blank=True, null=True)
    time = models.IntegerField(help_text="Time in minutes", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["done", "deadline"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.description)[:50]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description