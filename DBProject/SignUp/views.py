from django.shortcuts import render
from django import forms
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("<h1>Please Create an Account</h1>")
    #return HttpResponse("<h1>Please Create an Account</h1><p>Username:</p><input name=\"username\"></input><br><p>Password</p><input name=\"password\"></input><br><br><button name=\"submit\">Sign up!</button>")
