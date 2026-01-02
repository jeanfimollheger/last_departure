from django.urls import path
from .views import SnippetListView, SnippetDetailView, SnippetCreateView, SnippetUpdateView, SnippetDeleteView

urlpatterns = [
    path('', SnippetListView.as_view(), name='snippet_list'),
    path('new/', SnippetCreateView.as_view(), name='snippet_create'),
    path('<slug:slug>/edit/', SnippetUpdateView.as_view(), name='snippet_update'),
    path('<slug:slug>/delete/', SnippetDeleteView.as_view(), name='snippet_delete'),
    path('<slug:slug>/', SnippetDetailView.as_view(), name='snippet_detail'),
]  