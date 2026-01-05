# CREATION de l'ENVIRONNEMENT VIRTUEL

#bash
python3 -m venv venv

# SOURCER l'environnement virtuel

bash
source venv/bin/activate

# Upgrade PIP

(venv)
python -m pip install --upgrade pip

# Install django

(venv)
pip install django

# VERIFICATION de l'install

(venv)
django-admin --version

# FIGER les dépendances (7)

(venv)
pip freeze > requirements.txt

# CREATION du PROJET holding (8)

(venv)
django-admin startproject holding .

# CREATION de l'APP accounts (9)

(venv)
python manage.py startapp accounts

#CREATION du MODEL dans accounts CustomUser

## holding/settings.py (10)

INSTALLED_APPS = [
...,
'accounts',
]

## accounts/models.py (11)

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
pass
##accounts/models.py##

DECLARATION dans les settings de la nouvelle app accounts

DECLARATION du AUTH_USER_MODEL dans les settings
AUTH_USER_MODEL = 'accounts.CustomUser'
##holding/settings.py##

Les PREMIERES MIGRATIONS
python manage.py makemigrations
python manage.py migrate

ADMINISTRATION et SUPERUSER

## accounts/admin.py

from django.contrib import admin
from .models import CustomUser

admin.site.register(CustomUser)

## accounts/admin.py

CREATION du superuser
(venv)
python manage.py createsuperuser
"Username: jeanfi_dev
Email address: jpmh@gmx.fr
Password:
Password (again):
Superuser created successfully."

TEST obligatoire en allant sur le serveur et dans l'admin
(venv)
python manage.py runserver
En allant dans l'adim et en cliquant sur son superuser on doit voir dans l'adresse quelque comme : http://127.0.0.1:8000/admin/accounts/customuser/1/change/
et cela veut dire que c'est bien un model CustomUser qui est bien utilisé et non un User comme par défaut.

### Github

repository créé sur Github de jeanfimollheger
invitation envoyé à jeanfimh ...
qu'il accepte en double cliquant dessus
dans le directory (ici last_departure)
(venv) git init
sur le github de jeanfimollheger dans le repository concerné dans "code" copié le https
(ici -> https://github.com/jeanfimollheger/last_departure.git)
(venv) git init
(venv) git add README.md
(venv) git commit -m "first commit"
(venv) git branch -M main
(venv) git remote add origin https://github.com/jeanfimollheger/last_departure.git
(venv) git push -u origin main

# MISE EN PLACE du LOGIN et du LOGOUT

" plan global :

- les URLs d'authentification
- templates(login/base)
- parametres dans holding/settings.py
- test final "

## AJOUTER les urls d'authentification

## holding/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
path('admin/', admin.site.urls),
path('accounts/', include('django.contrib.auth.urls')),
]
##holding/urls.py##

# CREATION du templates global

A la racine templates/registration/login.html

# CONFIGURATION des templates dans settings.py

TEMPLATES = [
{
...
'DIRS': [BASE_DIR / 'templates'],
...
},
]

# login.html

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Connexion</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="container py-5">

<h2>Connexion</h2>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary">Se connecter</button>
</form>

</body>
</html>

# CONFIGURATION PARAMETRES LOGIN et LOGOUT dans settings.py

holding/settings.py
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

# CREATION VIEW home dans accounts/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
return render(request, "accounts/home.html")

# CREATION de urls.py dans accounts

from django.urls import path, include
from .views import home

urlpatterns = [
path("", home, name="home"),
]

# INTEGRATION de accounts/urls.py dans holding/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
path('admin/', admin.site.urls),
path('accounts/', include('django.contrib.auth.urls')),
path('', include('accounts.urls')),
]

# CREATION de home.html dans accounts/templates/accounts

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Home</title>
</head>
<body>
 <h1>Bienvenue {{ user.username }}</h1>

<p>Tu es connecté.</p>

<a href="{% url 'logout' %}">Se déconnecter</a>

</body>
</html>
##########################################
DEUXIEME APP : snippets
Creation app
settings INSTALLED_APPS
CREATION du model Snippet
ADMINISTRATION du model Snippet
... makemigrations
... migrate

# CLASS BASED VIEWS

snippets/views.py

## ListView

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Snippet

class SnippetListView(ListView):
model = Snippet
template_name = 'snippets/snippet_list.html'
context_object_name = 'snippets'

## urls de snippets/urls.py

from django.urls import path
from .views import SnippetListView, SnippetDetailView

url_patterns = [
path('', SnippetListView.as_view(), name='snippet_list'),
path('<slug:slug>/', SnippetDetailView.as_view(), name='snippet_detail'),
]

## urls de holding/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
path('admin/', admin.site.urls),
path('accounts/', include('django.contrib.auth.urls')),
path('', include('accounts.urls')),
path('snippets/', include('snippets.urls')),
]

## DetailView

class SnippetDetailView(DetailView):
model = Snippet
template_name = "snippets/snippet_detail.html"
context_object_name = "snippet" # ces 2 lignes ci-dessous ne sont pas nécessaires mais expliquent # que l'attribut slug du model est le slug_field # et que dans l'url ce sera aussi slug
slug_field = "slug"
slug_url_kwarg = "slug"

## detail_form.html

{% extends "base.html" %}

{% block title %}Snippet{% endblock %}

{% block content %}

<h1>{{ view.object|default:"New snippet" }}</h1>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button class="btn btn-secondary">Save</button>
</form>
{% endblock %}

## RETOUCHE base.html

A COMPLETER

## CreateView

class SnippetCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
model = Snippet
fields = ["title", "code", "order"]
template_name = "snippets/snippet_form.html"
success_url = reverse_lazy("snippet_list")

    def test_func(self):
        return self.request.user.is_superuser

## UpdateView

class SnippetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
model = Snippet
fields = ["title", "code", "order"]
template_name = "snippets/snippet_form.html"
slug_field = "slug"
slug_url_kwarg = "slug"
success_url = reverse_lazy("snippet_list")

    def test_func(self):
        return self.request.user.is_superuser

## Retouche snippet_detail.html

A COMPLETER

## Deleview

class SnippetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
model = Snippet
template_name = "snippets/snippet_confirm_delete.html"
slug_field = "slug"
slug_url_kwarg = "slug"
success_url = reverse_lazy("snippet_list")

    def test_func(self):
        return self.request.user.is_superuser
