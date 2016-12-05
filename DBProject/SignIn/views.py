from django import forms
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

import sqlite3
import bcrypt
import os

# Create your views here.
def login(request):
    if request.method == 'POST':
        try:
            if('uname' in request.session):
                html = "<h1>Already Logged In as " + str(request.session.get('uname')) + "</h1>"
                return HttpResponse(html)


            uname = request.POST.get('username',None)
            pwd = request.POST.get('password',None)

            conn = sqlite3.connect(os.path.join('RMHS.db'))
            c = conn.cursor()

            c.execute('SELECT * FROM Credentials WHERE c_credentialKey = ?',(uname,))
            row = c.fetchone()

            html = "<h1>Username or Password are Invalid</h1>"
            if(row is not None):
                (uname,pwdInDb,salt) = row
                if(bcrypt.hashpw(pwd.encode('UTF-8'),salt.encode('UTF-8')) == pwdInDb):
                    html = "<h1>Password Matches, Logged In</h1>"
                    request.session['uname'] = uname

            conn.close()
            return HttpResponse(html)
        except:
            #redirect back to index if possible
            return render(request, 'signInForm.html')
    else:
        return render(request, 'signInForm.html')
