from django.contrib import admin
from .models import Snippet

# admin.site.register(Snippet)

@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'order', 'created_at',)
    prepopulated_fields = {"slug": ("title",)}
    