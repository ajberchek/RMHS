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
def checkFl(som):
    try:
        float(som)
        return 1
    except ValueError:
        return 0

def searchQ(request):
    zipCode = request.GET.get('zipcode', None)
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
    #if(len(minPrice) == 0 and len(maxPrice) == 0 and  len(ayear) == 0 and len(byear) == 0 and len(lstar) == 0 and  len(hstar) == 0 and len(minroom) == 0 and len(maxroom) == 0 and len(minbthm) == 0 and len(maxbthm) == 0):
    #    return render(request, "noresult.html")

    if(len(minPrice) == 0):
        minPrice = 0
    if(len(maxPrice) == 0):
        maxPrice = 99999999
    if(len(ayear) == 0):
        ayear = 0
    if(len(byear) == 0):
        byear = 99999999
    if(len(lstar) == 0):
        lstar = -5
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
    if(checkInt(minroom) == 0 or checkInt(maxPrice) == 0 or checkInt(ayear) == 0 or checkInt(byear) == 0 or checkFl(lstar) == 0 or checkFl(hstar) == 0 or checkInt(minroom) == 0 or checkInt(maxroom) == 0 or checkInt(minbthm) == 0 or  checkInt(maxbthm) == 0):
        return render(request, "noresult.html")

    if(int(minPrice) <= int(maxPrice)):
        if(int(ayear) <= int(byear)):
            if(float(lstar) <=  float(hstar)):
                if(int(minroom) <= int(maxroom)):
                    if(int(minbthm) <= int(maxbthm)):
                        conn = sqlite3.connect(os.path.join('RMHS.db'))
                        c = conn.cursor()
                        html = ''
                        minPrice = int(minPrice)
                        maxPrice = int(maxPrice)

                        ayear = int(ayear)
                        byear = int(byear)

                        lstar = float(lstar)
                        hstar = float(hstar)

                        minroom = int(minroom)
                        maxroom = int(maxroom)

                        minbthm = int(minbthm)
                        maxbthm = int(maxbthm)
                        #dic = {}       //adding avg to dic

                        #for row in c.execute("SELECT avg(rv_rating), r_realtorKey FROM Realtor, Reviews WHERE rv_realtorkey = r_realtorKey GROUP BY r_realtorKey"):
                        #    dic[row[1]] = row[0]
                        #for row in dic:
                        #    print(dic[row])

                        count = 0
                        html = "<a style=\"text-align: right; align: right; float: right;\" href=\"../home/\">Home</a>"


                        html += "<!-- Latest compiled and minified CSS --><link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\" integrity=\"sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u\" crossorigin=\"anonymous\"><!-- Optional theme --><link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css\" integrity=\"sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp\" crossorigin=\"anonymous\"><!-- Latest compiled and minified JavaScript --><script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js\" integrity=\"sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa\" crossorigin=\"anonymous\"></script>"


                        html += "<h1>Search Results(Click Picture For More Details):</h1>"
                        if(len(zipCode) != 0):
                            zipCode = int(zipCode)
                            for row in c.execute('SELECT distinct h_housekey,p_name FROM House as H, Pictures ' +
                                                'Where H.h_location = ? and p_name in (SELECT p_name ' +
                                                                'FROM House, Pictures, Realtor, Manages, Reviews ' +
                                                                'WHERE H.h_housekey = h_housekey and ' +
                                                                'h_housekey = p_houseKey and r_realtorKey = m_realtor ' +
                                                                'and r_realtorKey = rv_realtorkey and m_housekey = h_housekey ' +
                                                                'and h_price >= ? and h_price <= ? and h_constructionyear >= ? ' +
                                                                'and h_constructionyear <= ? and ? <= (SELECT avg(rv2.rv_rating) ' +
                                                                    'FROM Reviews as rv2 ' +
                                                                    'WHERE rv2.rv_realtorkey = r_realtorKey) ' +
                                                                'and ? >= (SELECT avg(rv2.rv_rating) ' +
                                                                        'FROM Reviews as rv2 ' +
                                                                        'WHERE rv2.rv_realtorkey = r_realtorKey) ' +
                                                                'and h_numRooms >= ? and h_numRooms <= ? ' +
                                                                'and h_numBath >= ? and ' +
                                                                'h_numBath <= ? LIMIT 1)',(zipCode, minPrice,maxPrice,ayear, byear, lstar, hstar, minroom, maxroom, minbthm, maxbthm)):
                                print("hiaaaaa")
                                print(row)
                                html += "<li><a href=../home/ViewHouse?h_housekey=" + str(row[0]) + "><img src = \""+ str(row[1]) +"\" height=\"256\" </img><br></a></li>"
                                count += 1
                        else:
                            for row in c.execute('SELECT distinct h_housekey,p_name FROM House as H, Pictures ' +
                                                'Where p_name in (SELECT p_name ' +
                                                                'FROM House, Pictures, Realtor, Manages, Reviews ' +
                                                                'WHERE H.h_housekey = h_housekey and ' +
                                                                'h_housekey = p_houseKey and r_realtorKey = m_realtor ' +
                                                                'and r_realtorKey = rv_realtorkey and m_housekey = h_housekey ' +
                                                                'and h_price >= ? and h_price <= ? and h_constructionyear >= ? ' +
                                                                'and h_constructionyear <= ? and ? <= (SELECT avg(rv2.rv_rating) ' +
                                                                    'FROM Reviews as rv2 ' +
                                                                    'WHERE rv2.rv_realtorkey = r_realtorKey) ' +
                                                                'and ? >= (SELECT avg(rv2.rv_rating) ' +
                                                                        'FROM Reviews as rv2 ' +
                                                                        'WHERE rv2.rv_realtorkey = r_realtorKey) ' +
                                                                'and h_numRooms >= ? and h_numRooms <= ? ' +
                                                                'and h_numBath >= ? and ' +
                                                                'h_numBath <= ? LIMIT 1)',(minPrice,maxPrice,ayear, byear, lstar, hstar, minroom, maxroom, minbthm, maxbthm)):
                                html += "<li><a href=../home/ViewHouse?h_housekey=" + str(row[0]) + "><img src = \""+ str(row[1]) +"\" height=\"256\" </img><br></a></li>"
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
