from django.shortcuts import render


def index(request):
    return render(request, 'autoxl/index.html')


def go(request):
    pass

