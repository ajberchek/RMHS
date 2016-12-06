from django import forms
from django.http import *
from django.template import loader
from django.shortcuts import render

import sqlite3
import bcrypt
import os

# Create your views here.
def login(request):
    if request.method == 'POST':
        print("first")
        try:
            if('uname' in request.session):
                return HttpResponseRedirect("../Account")


            uname = request.POST.get('username',None)
            pwd = request.POST.get('password',None)

            conn = sqlite3.connect(os.path.join('RMHS.db'))
            c = conn.cursor()

            c.execute('SELECT * FROM Credentials WHERE c_credentialKey = ?',(uname,))
            row = c.fetchone()

            if(row is not None):
                (uname,pwdInDb,salt,typeChoice) = row
                if(bcrypt.hashpw(pwd.encode('UTF-8'),salt.encode('UTF-8')) == pwdInDb):
                    request.session['uname'] = uname
                    request.session['type'] = typeChoice
                    return HttpResponseRedirect("../Account")

            conn.close()
            return render(request, 'signInForm.html')
        except:
            #redirect back to index if possible
            return render(request, 'signInForm.html')
    else:
        print("doesitgohere")
        return render(request, 'signInForm.html')
