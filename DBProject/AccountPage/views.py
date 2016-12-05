from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from django.template import loader

import sqlite3
import os

def accountPage(request):
    cont = {'realtorName':request.session.get('uname',None),'utype':request.session.get('type',None)}
    return render(context=cont,request=request,template_name='accountPage.html')

def editAccount(request):
    return HttpResponse("")
