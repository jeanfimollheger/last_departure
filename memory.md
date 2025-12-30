#CREATION de l'ENVIRONNEMENT VIRTUEL
bash
python3 -m venv venv
#SOURCER l'environnement virtuel
bash
source venv/bin/activate
#Upgrade PIP
(venv)
python -m pip install --upgrade pip
#Install django
(venv)
pip install django
#VERIFICATION de l'install
(venv)
django-admin --version
#FIGER les dépendances
(venv)
pip freeze > requirements.txt
#CREATION du PROJET holding
(venv)
django-admin startproject holding .
#CREATION de l'APP accounts
(venv)
python manage.py startapp accounts

#CREATION du MODEL dans accounts CustomUser
##accounts/models.py
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
pass
##accounts/models.py

DECLARATION dans les settings de la nouvelle app accounts
##holding/settings.py
INSTALLED_APPS = [
...,
'accounts',
]
DECLARATION du AUTH_USER_MODEL dans les settings
AUTH_USER_MODEL = 'accounts.CustomUser'
##holding/settings.py

Les PREMIERES MIGRATIONS
python manage.py makemigrations
python manage.py migrate

ADMINISTRATION et SUPERUSER
##accounts/admin.py
from django.contrib import admin
from .models import CustomUser

admin.site.register(CustomUser)
##accounts/admin.py

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
(venv) git remote add origin https://github.com/jeanfimollheger/last_departure.git
(venv) git status
(venv) git add .
(venv) git commit -m "first commit"
