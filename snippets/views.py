from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Snippet
from django.db.models.functions import Coalesce
from django.db.models import Q

# Create your views here.
class SnippetListView(ListView):
    model = Snippet
    template_name = 'snippets/snippet_list.html'
    context_object_name = 'snippets'
    
    def get_queryset(self):
        qs = (
            Snippet.objects
            .annotate(has_order=Coalesce("order", 999999))
            .order_by("has_order", "-created_at")
        )

        query = self.request.GET.get("q")
        if query:
            keywords = query.split()
            q_object = Q()
            for word in keywords:
                q_object &= (
                    Q(title__icontains=word) |
                    Q(description__icontains=word) |
                    Q(code__icontains=word)
                )
            qs = qs.filter(q_object)

        return qs
"""
    def get_queryset(self):
        return (
            Snippet.objects
            .annotate(
                has_order=Coalesce("order", 999999)
            )
            .order_by("has_order", "-created_at")
        )
"""

class SnippetDetailView(DetailView):
    model = Snippet
    template_name = "snippets/snippet_detail.html"
    context_object_name = "snippet"
    # ces 2 lignes ci-dessous ne sont pas nécessaires mais expliquent
    # que l'attribut slug du model est le slug_field
    # et que dans l'url ce sera aussi slug
    slug_field = "slug"
    slug_url_kwarg = "slug"

class SnippetCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Snippet
    fields = ["title","location", "code", "description", "order"]
    template_name = "snippets/snippet_form.html"
    success_url = reverse_lazy("snippet_list")

    def test_func(self):
        return self.request.user.is_superuser

class SnippetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Snippet
    fields = ["title", "location", "code", "description", "order"]
    template_name = "snippets/snippet_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("snippet_list")

    def test_func(self):
        return self.request.user.is_superuser

class SnippetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Snippet
    template_name = "snippets/snippet_confirm_delete.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("snippet_list")

    def test_func(self):
        return self.request.user.is_superuser