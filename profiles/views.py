from django.shortcuts import render
from django.views import generic
# Create your views here.


def register(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def login(request)