from django.shortcuts import render

from learners.models import LearnerRegister


def index(request):
    return render(request, 'index.html')


def tables(request):
    learners = LearnerRegister.objects.all()
    return render(request, 'tables.html', {'learners': learners})


def login(request):
    return render(request, 'auth/login.html')


def register(request):
    return render(request, 'auth/register.html')
