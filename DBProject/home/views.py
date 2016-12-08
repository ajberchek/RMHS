from django.shortcuts import render
from django import forms
from django.http import *
from django.template import loader

import sqlite3
import os

class House:
    def __init__(self,houseID,mainPicURL):
            self.ID = houseID
            self.thumbnail = mainPicURL

def viewHome(request):
    if('uname' in request.session):
        html = "<form method=\"GET\" action=\"../rsearch/\">"
        html += "<button type=\"submit\">Search</button><br></form>"
        return HttpResponse(html)
    return render(request,'homepage.html')

def viewHouse(request):
    if request.method == 'GET':
        picUrlList = []
        conn = sqlite3.connect('RMHS.db')
        houseCursor = conn.cursor()
        picCursor = conn.cursor()

        try:
            houseKey = request.GET.get('h_housekey',None)
            for row in picCursor.execute('SELECT p_name FROM Pictures WHERE p_houseKey = ?',(houseKey,)):
                picUrlList.append(row[0])
            houseCursor.execute('SELECT * FROM House WHERE h_housekey = ?',(houseKey,))
            row = houseCursor.fetchone()

            HouseKey = row[0]
            ConstructionYear = row[1]
            PetFriendly = row[2]
            NumRooms = row[3]
            NumBath = row[4]
            HouseSize = row[5]
            Appliances = row[6]
            SellStatus = row[7]
            Price = row[8]
            Garage = row[9]
            Description = row[10]
            AdditionalInfo = row[11]
            Address = row[12]
            Location = row[13]

            print(houseKey)
            print(HouseKey)

            cont = {'house_id':houseKey,'Pictures':picUrlList,'HouseKey':HouseKey,'ConstructionYear':ConstructionYear,'PetFriendly':PetFriendly,'NumRooms':NumRooms,'NumBath':NumBath,'HouseSize':HouseSize,'Appliances':Appliances,'SellStatus':SellStatus,'Price':Price,'Garage':Garage,'Description':Description,'AdditionalInfo':AdditionalInfo,'Address':Address,'Location':Location}
            return render(context=cont,request=request,template_name='viewHouse.html')
        except:
            raise Http404()
