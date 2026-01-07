from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime


# Create your views here.
@login_required
def home(request):
    context = {'date': datetime.now()}
    return render(request, "accounts/home.html", context)
