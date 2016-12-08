from django.shortcuts import render
from django import forms
from django.http import *
from django.template import loader

def index(request):
    return render(request, 'search.html')
