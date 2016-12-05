from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def createAccount(request):
    if request.method == 'POST':
        uname = request.POST.get('username',None)
        pwd = request.POST.get('password',None)
        pwdVerify = request.POST.get('passwordVerify',None)
        try:
            html = ("<H1>Pass: " + pwd + "</H1>")
            return HttpResponse(html)
        except:
            #redirect back to index if possible
            return render(request, 'signUpForm.html')
    else:
        return render(request, 'signUpForm.html')
        
