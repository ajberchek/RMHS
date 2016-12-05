from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from django.template import loader

import sqlite3
import bcrypt
import os

# Create your views here.
def createAccount(request):
    if request.method == 'POST':
        try:
            uname = request.POST.get('username',None)
            pwd = request.POST.get('password',None)
            pwdVerify = request.POST.get('passwordVerify',None)
            typeChoice = request.POST.get('type',None)

            conn = sqlite3.connect(os.path.join('RMHS.db'))
            c = conn.cursor()

            c.execute('SELECT * FROM Credentials WHERE c_credentialKey = ?',(uname,))
            row = c.fetchone()

            if(pwd != pwdVerify):
                html = "<h1>PWDs DONT MATCH</h1>"
            else:
                html = "<h1>USER ALREADY EXISTS</h1>"
                if(row is None):
                    salt = bcrypt.gensalt()
                    hashedPw = bcrypt.hashpw(pwd.encode('UTF-8'),salt)
                    c.execute('INSERT INTO Credentials VALUES (?,?,?,?)',(uname,hashedPw,salt,typeChoice))
                    html = "<h1>ADDED USER</h1>"
                    conn.commit()
                    request.session['uname'] = uname
                    request.session['type'] = typeChoice

            conn.close()
            return HttpResponse(html)
        except:
            #redirect back to index if possible
            return render(request, 'signUpForm.html')
    else:
        return render(request, 'signUpForm.html')
        
