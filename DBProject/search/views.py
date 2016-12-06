from django import forms
from django.http import *
from django.template import loader
from django.shortcuts import render

import sqlite3
import os

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

    conn = sqlite3.connect(os.path.join('RMHS.db'))
    c = conn.cursor()
    html = ''

    for row in c.execute('SELECT distinct p_name, h_housekey FROM House, Pictures, Realtor, Manages, Reviews WHERE h_housekey = p_houseKey and r_realtorKey = m_realtor and r_realtorKey = rv_realtorkey and m_housekey = h_housekey and h_price >= ? and h_price <= ? and h_constructionyear >= ? and h_constructionyear <= ? and rv_rating >= ? and rv_rating <= ? and h_numRooms >= ? and h_numRooms <= ? and h_numBath >= ? and h_numBath <= ?',(minPrice,maxPrice,ayear, byear, lstar, hstar, minroom, maxroom, minbthm, maxbthm)):
        if(row is not None):
            html += "<a href=../home/ViewHouse?h_housekey=" + str(row[1]) + "><img src = \""+ str(row[0]) +"\" height=\"50\" width=\"50\" </img><br></a>"
        else:
            html += "<h1>None Found</h1>"
            break

    return HttpResponse(html)
