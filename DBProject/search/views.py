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

    for row in c.execute('SELECT distinct h_housekey,p_name FROM House as H, Pictures Where p_name in (SELECT p_name FROM House, Pictures, Realtor, Manages, Reviews WHERE H.h_housekey = h_housekey and h_housekey = p_houseKey and r_realtorKey = m_realtor and r_realtorKey = rv_realtorkey and m_housekey = h_housekey and h_price >= ? and h_price <= ? and h_constructionyear >= ? and h_constructionyear <= ? and rv_rating >= ? and rv_rating <= ? and h_numRooms >= ? and h_numRooms <= ? and h_numBath >= ? and h_numBath <= ? LIMIT 1)',(minPrice,maxPrice,ayear, byear, lstar, hstar, minroom, maxroom, minbthm, maxbthm)):
        if(row is not None):
            html += "<li><a href=../home/ViewHouse?h_housekey=" + str(row[0]) + "><img src = \""+ str(row[1]) +"\" height=\"256\" </img><br></a></li>"
        else:
            break
    if(html == ''):
        html += "<h1>None Found</h1>"

    return HttpResponse(html)
