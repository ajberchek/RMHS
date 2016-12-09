from django import forms
from django.http import *
from django.template import loader
from django.shortcuts import render

import sqlite3
import bcrypt
import os

# Create your views here.
def logout(request):
    if request.method == 'GET':
        try:
            if('uname' in request.session):
                html = "<h1>Successfully Logged Out " + str(request.session.get('uname')) + "</h1>"
                request.session.delete('uname')

            return HttpResponseRedirect("../home")
        except:
            #redirect back to index if possible
            return HttpResponseRedirect("../home")
    else:
            return HttpResponseRedirect("../home")
