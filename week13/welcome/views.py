from curses.ascii import HT
from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.

def greet(request):
    return HttpResponse("hello world")