from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from django.template import loader
import sqlite3
import os

# Create your views here.
def viewHome(request):

    #html = ''
    #conn = sqlite3.connect(os.path.join('RMHS.db'))
    #c = conn.cursor()

    #for row in c.execute('SELECT p_name FROM House, Pictures where h_housekey = p_houseKey'):
    #    html += '<img src = '+ str(row)[2:len(str(row))-3] +'height="42" width="42" </img>'
    #
    #conn.close()

    return HttpResponse(render(request, 'homepage.html'))
