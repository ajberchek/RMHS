from django import forms
from django.http import *
from django.template import loader
from django.shortcuts import render

import sqlite3
import os
def checkInt(som):
    try:
        int(som)
        return 1
    except ValueError:
        return 0

def searchQ(request):
    minPrice = request.GET.get('minPrice', None)
    maxPrice = request.GET.get('maxPrice', None)
    ayear = request.GET.get('ayear', None)
    byear = request.GET.get('byear', None)
    lstar = request.GET.get('lstar', None)
    hstar = request.GET.get('hstar', None)
    minroom = request.GET.get('minroom', None)
    maxroom = request.GET.get('maxroom', None)
    minbthm = request.GET.get('minbthm', None)
    maxbthm = request.GET.get('maxbthm', None)
    #print("yest"+minPrice)
    if(len(minPrice) == 0 and len(maxPrice) == 0 and  len(ayear) == 0 and len(byear) == 0 and len(lstar) == 0 and  len(hstar) == 0 and len(minroom) == 0 and len(maxroom) == 0 and len(minbthm) == 0 and len(maxbthm) == 0):
        return render(request, "noresult.html")

    if(len(minPrice) == 0):
        minPrice = 0
    if(len(maxPrice) == 0):
        maxPrice = 99999999
    if(len(ayear) == 0):
        ayear = 0
    if(len(byear) == 0):
        byear = 99999999
    if(len(lstar) == 0):
        lstar = 0
    if(len(hstar) == 0):
        hstar = 5
    if(len(minroom) == 0):
        minroom = 0
    if(len(maxroom) == 0):
        maxroom = 99999999
    if(len(minbthm) == 0):
        minbthm = 0
    if(len(maxbthm) == 0):
        maxbthm = 99999999
    if(checkInt(minroom) == 0 or checkInt(maxPrice) == 0 or checkInt(ayear) == 0 or checkInt(byear) == 0 or checkInt(lstar) == 0 or checkInt(hstar) == 0 or checkInt(minroom) == 0 or checkInt(maxroom) == 0 or checkInt(minbthm) == 0 or  checkInt(maxbthm) == 0):
        return render(request, "noresult.html")

    if(int(minPrice) <= int(maxPrice)):
        if(int(ayear) <= int(byear)):
            if(int(lstar) <=  int(hstar)):
                if(int(minroom) <= int(maxroom)):
                    if(int(minbthm) <= int(maxbthm)):
                        conn = sqlite3.connect(os.path.join('RMHS.db'))
                        c = conn.cursor()
                        html = ''
                        minPrice = int(minPrice)
                        maxPrice = int(maxPrice)

                        ayear = int(ayear)
                        byear = int(byear)

                        lstar = int(lstar)
                        hstar = int(hstar)

                        minroom = int(minroom)
                        maxroom = int(maxroom)

                        minbthm = int(minbthm)
                        maxbthm = int(maxbthm)

                        count = 0
                        for row in c.execute('SELECT distinct h_housekey,p_name FROM House as H, Pictures Where p_name in (SELECT p_name FROM House, Pictures, Realtor, Manages, Reviews WHERE H.h_housekey = h_housekey and h_housekey = p_houseKey and r_realtorKey = m_realtor and r_realtorKey = rv_realtorkey and m_housekey = h_housekey and h_price >= ? and h_price <= ? and h_constructionyear >= ? and h_constructionyear <= ? and rv_rating >= ? and rv_rating <= ? and h_numRooms >= ? and h_numRooms <= ? and h_numBath >= ? and h_numBath <= ? LIMIT 1)',(minPrice,maxPrice,ayear, byear, lstar, hstar, minroom, maxroom, minbthm, maxbthm)):
                            html += "<a href=../home/ViewHouse?h_housekey=" + str(row[0]) + "><img src = \""+ str(row[1]) +"\" height=\"50\" width=\"50\" </img><br></a>"
                            count += 1

                        if(count == 0):
                                return render(request, "noresult.html")

                        return HttpResponse(html)
                    else:
                        html = "<h3>Error: Minimum Bathrooms cannot be more than Maximum Bathrooms</h3>"
                        return HttpResponseRedirect("../rsearch")
                else:
                    html = "<h3>Error: Minimum rooms can't be higher then Maximum rooms</h3>"
                    return HttpResponseRedirect("../rsearch")
            else:
                html = "<h3>Error: Lower rating are higher than Upper rating</h3>"
                return HttpResponseRedirect("../rsearch")
        else:
            html = "<h3>Error: Built before cannot be after built after</h3>"
            return HttpResponseRedirect("../rsearch")
    else:
        html = "<h3>Error: Minimum is more than maximum</h3>"
        return HttpResponseRedirect("../rsearch")
