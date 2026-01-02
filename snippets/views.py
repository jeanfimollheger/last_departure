from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Snippet

# Create your views here.
class SnippetListView(ListView):
    model = Snippet
    template_name = 'snippets/snippet_list.html'
    context_object_name = 'snippets'

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
    fields = ["title", "code", "order"]
    template_name = "snippets/snippet_form.html"
    success_url = reverse_lazy("snippet_list")

    def test_func(self):
        return self.request.user.is_superuser

class SnippetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Snippet
    fields = ["title", "code", "order"]
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