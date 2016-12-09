from django.shortcuts import render
from django import forms
from django.http import *
from django.template import loader

import sqlite3
import os

def CreateServiceProvder(request):
    print(request.session.get('type'))
    if request.method == 'GET':
        if('type' in request.session and request.session.get('type') == 'S'):
            try:
                return render(request=request,template_name='createServiceProvider.html')
            except Exception as e:
                print(e)
                raise Http404()
    elif request.method == 'POST':
        if('type' in request.session and request.session.get('type') == 'S'):
            conn = sqlite3.connect('RMHS.db')
            spCursor = conn.cursor()
            servicesCursor = conn.cursor()
            servicesCursorInsert = conn.cursor()

            try:
                ServiceProviderName = request.POST.get('ServiceProviderName',None)
                CredentialKey = request.session.get('uname')
                Location = request.POST.get('Location',None)
                ContactInfo = request.POST.get('ContactInfo',None)
                ServiceType = request.POST.get('ServiceType',None)

                if(ServiceProviderName is None or len(ServiceProviderName) == 0):
                    return HttpResponseRedirect("")

                #spCursor.execute('SELECT * FROM ServiceProvider WHERE s_name=? AND s_credentialKey=?',(ServiceProviderName,CredentialKey))
                #if(spCursor.fetchone() is not None):
                #    #Service Provider or User exists already in the service provider database
                #    return Http404("<h6>User is already in charge of a Service Provider, or Service Provider name is taken, go back and try again</h6>")

                spCursor.execute('SELECT max(s_providerKey) FROM ServiceProvider;')
                (ProviderKey) = spCursor.fetchone()
                if(ProviderKey is None):
                    ProviderKey = 0
                else:
                    if(ProviderKey[0] is None):
                        ProviderKey = 0
                    else:
                        ProviderKey = ProviderKey[0] + 1
                
                spCursor.execute('INSERT INTO ServiceProvider VALUES(?,?,?,?,?,?)',(ProviderKey,ServiceProviderName,ServiceType,Location,ContactInfo,CredentialKey))

                for House in servicesCursor.execute('SELECT h_housekey FROM House WHERE h_location=?',(Location,)):
                    servicesCursorInsert.execute('INSERT INTO Services VALUES(?,?)',(House[0],ProviderKey))
                
                

                conn.commit()
                conn.close()

                #redirect back ot the editing page
                return HttpResponseRedirect("../Account")
            except Exception as e:
                print(e)
                return HttpResponse("<h6>Please go back and enter all data after having signed in as a Service Provider")

        raise Http404("Not a Service Provider")
    raise Http404("")

def ViewServices(request):
    if(request.method == 'GET'):
        try:
            conn = sqlite3.connect('RMHS.db')
            spCursor = conn.cursor()

            CredentialKey = request.GET.get('s_credentialKey')


            html = ""
            for SP in spCursor.execute('SELECT s_name,s_ServiceType,s_providerKey FROM ServiceProvider WHERE s_credentialKey=?',(CredentialKey,)):
                if(len(html) == 0):
                    html = "<a href=\"../home\">Home</a><a href=\"../Logout\"> Logout</a>"
                    html += "<h2>Services Managed By: " + str(CredentialKey) + "</h2>"
                html += "<li><h4><a href=\"ViewService?s_providerKey=" + str(SP[2]) + "\">" + str(SP[0]) + ": " + str(SP[1]) + "</a></h4></li>"

            if(len(html) == 0):
                html = "<a href=\"../home\">Home</a><a href=\"../Logout\">Logout</a>"
                html += "<h6>No Services Managed By: " + str(CredentialKey) + "</h6>"

            if('type' in request.session and request.session.get('type') == 'S'):
                html += "<form method=\"GET\" action=\"CreateServiceProvider\"><button type=\"submit\">Add Service</button></form>"

            return HttpResponse(html)
        except Exception as e:
            print(e)
            return HttpResponse(html)
    raise Http404()

def ViewService(request):
    if(request.method == 'GET'):
        try:
            conn = sqlite3.connect('RMHS.db')
            spCursor = conn.cursor()

            ProviderKey = request.GET.get('s_providerKey')

            spCursor.execute('SELECT * FROM ServiceProvider WHERE s_providerKey=?',(ProviderKey,))
            (spData) = spCursor.fetchone()
            if(spData is None):
                raise Http404("Invalid Service Provider Name")
            else:
                ServiceProviderName = spData[1]
                ServiceType = spData[2]
                Location = spData[3]
                ContactInfo = spData[4]

                cont = {'Name':ServiceProviderName,'ServiceType':ServiceType,'Location':Location,'ContactInfo':ContactInfo}
                return render(context=cont,request=request,template_name="viewService.html")
        except Exception as e:
            print(e)
            raise Http404("")

    raise Http404("")
