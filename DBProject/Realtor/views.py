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

def housePage(request):
    if('type' in request.session and request.session.get('type') == 'R'):
        listOfHouses = []
        conn = sqlite3.connect('RMHS.db')
        realtorCursor = conn.cursor()
        houseCursor = conn.cursor()
        picCursor = conn.cursor()

        realtorCursor.execute('SELECT distinct r_realtorKey FROM Realtor WHERE r_credentialKey = ?',(request.session.get('uname'),))
        (realtorKey) = realtorCursor.fetchone()
        print(realtorKey)

        for row in houseCursor.execute('SELECT h_housekey FROM House,Manages WHERE h_housekey = m_housekey AND m_realtor = ?',realtorKey):
            (housekey) = row
            picCursor.execute('SELECT p_name FROM Pictures WHERE p_houseKey = ? LIMIT 1',housekey)
            (picUrl) = picCursor.fetchone()[0]
            print("HouseKey: " + str(housekey[0]) + "URL: " + str(picUrl))
            h = House(housekey[0],picUrl)
            listOfHouses.append(h)

        cont = {'realtorName':request.session.get('uname',None),'house_list':listOfHouses}
        return render(context=cont,request=request,template_name='realtorHouses.html')
    raise Http404("Not a Realtor")

def editHouse(request):
    if request.method == 'GET':
        if('type' in request.session and request.session.get('type') == 'R'):
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

                Address = row[0]
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

                cont = {'house_id':houseKey,'Pictures':picUrlList,'Address':Address,'ConstructionYear':ConstructionYear,'PetFriendly':PetFriendly,'NumRooms':NumRooms,'NumBath':NumBath,'HouseSize':HouseSize,'Appliances':Appliances,'SellStatus':SellStatus,'Price':Price,'Garage':Garage,'Description':Description,'AdditionalInfo':AdditionalInfo,'Address':Address,'Location':Location}
                return render(context=cont,request=request,template_name='editHouse.html')
            except:
                raise Http404()
    elif request.method == 'POST':
        raise Http404("This is to update data")
    raise Http404("Not a Realtor")
