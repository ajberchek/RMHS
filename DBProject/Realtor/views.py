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

        for row in houseCursor.execute('SELECT h_housekey FROM House,Manages WHERE h_housekey = m_housekey AND m_realtor = ?',realtorKey):
            (housekey) = row
            picCursor.execute('SELECT p_name FROM Pictures WHERE p_houseKey = ? LIMIT 1',housekey)
            (picUrl) = picCursor.fetchone()
            if(picUrl is not None):
                picUrl = picUrl[0]
            else:
                picUrl = ""
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


                cont = {'house_id':houseKey,'Pictures':picUrlList,'HouseKey':HouseKey,'ConstructionYear':ConstructionYear,'PetFriendly':PetFriendly,'NumRooms':NumRooms,'NumBath':NumBath,'HouseSize':HouseSize,'Appliances':Appliances,'SellStatus':SellStatus,'Price':Price,'Garage':Garage,'Description':Description,'AdditionalInfo':AdditionalInfo,'Address':Address,'Location':Location}
                return render(context=cont,request=request,template_name='editHouse.html')
            except:
                raise Http404()
    elif request.method == 'POST':
        if('type' in request.session and request.session.get('type') == 'R'):
            conn = sqlite3.connect('RMHS.db')
            houseCursor = conn.cursor()
            picCursor = conn.cursor()
            realtorCursor = conn.cursor()

            try:
                HouseKey = request.POST.get('HouseKey',None)
                ConstructionYear = request.POST.get('ConstructionYear',None)
                PetFriendly = request.POST.get('PetFriendly',None)
                NumRooms = request.POST.get('NumRooms',None)
                NumBath = request.POST.get('NumBath',None)
                HouseSize = request.POST.get('HouseSize',None)
                Appliances = request.POST.get('Appliances',None)
                SellStatus = request.POST.get('SellStatus',None)
                Price = request.POST.get('Price',None)
                Garage = request.POST.get('Garage',None)
                Description = request.POST.get('Description',None)
                AdditionalInfo = request.POST.get('AdditionalInfo',None)
                Address = request.POST.get('Address',None)
                Location = request.POST.get('Location',None)


                #used to verify a realtor has permissions for this house
                realtorCursor.execute('SELECT distinct r_realtorKey FROM Realtor WHERE r_credentialKey = ?',(request.session.get('uname'),))
                realtorKey = realtorCursor.fetchone()[0]
                houseCursor.execute('SELECT h_housekey FROM House,Manages,Realtor WHERE h_housekey=? AND h_housekey=m_housekey AND m_realtor=?',(HouseKey,realtorKey))
                realtorOwnedHouseKey = houseCursor.fetchone()

                if(realtorOwnedHouseKey is not None):
                    #Since the realtor has edit permissions for this house, then we can edit it safely
                    houseCursor.execute('UPDATE House SET h_constructionyear=?,h_petFriendly=?,h_numRooms=?,h_numBath=?,h_size=?,h_appliances=?,h_sellStatus=?,h_price=?,h_garage=?,h_description=?,h_additionalInfo=?,h_address=?,h_location=? WHERE h_housekey=?',(ConstructionYear,PetFriendly,NumRooms,NumBath,HouseSize,Appliances,SellStatus,Price,Garage,Description,AdditionalInfo,Address,Location,HouseKey))
                    conn.commit()
                    conn.close()

                #redirect back ot the editing page
                return HttpResponseRedirect("EditHouse?h_housekey=" + str(HouseKey))
            except Exception as e:
                print(e)
                return HttpResponseRedirect("EditHouse?h_housekey=" + str(HouseKey))

        raise Http404("Not a Realtor")

def addHouse(request):
    if request.method == 'GET':
        if('type' in request.session and request.session.get('type') == 'R'):
            try:
                return render(request=request,template_name='createHouse.html')
            except:
                raise Http404()
    elif request.method == 'POST':
        if('type' in request.session and request.session.get('type') == 'R'):
            conn = sqlite3.connect('RMHS.db')
            houseCursor = conn.cursor()
            realtorCursor = conn.cursor()
            managesCursor = conn.cursor()

            try:
                houseCursor.execute('SELECT max(h_housekey) FROM House')
                (HouseKey) = houseCursor.fetchone()
                if(HouseKey is None):
                    HouseKey = 0
                else:
                    HouseKey = HouseKey[0] + 1
                ConstructionYear = request.POST.get('ConstructionYear',None)
                PetFriendly = request.POST.get('PetFriendly',None)
                NumRooms = request.POST.get('NumRooms',None)
                NumBath = request.POST.get('NumBath',None)
                HouseSize = request.POST.get('HouseSize',None)
                Appliances = request.POST.get('Appliances',None)
                SellStatus = request.POST.get('SellStatus',None)
                Price = request.POST.get('Price',None)
                Garage = request.POST.get('Garage',None)
                Description = request.POST.get('Description',None)
                AdditionalInfo = request.POST.get('AdditionalInfo',None)
                Address = request.POST.get('Address',None)
                Location = request.POST.get('Location',None)

                realtorCursor.execute('SELECT distinct r_realtorKey FROM Realtor WHERE r_credentialKey = ?',(request.session.get('uname'),))
                realtorKey = realtorCursor.fetchone()[0]
                houseCursor.execute('INSERT INTO House VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(HouseKey,ConstructionYear,PetFriendly,NumRooms,NumBath,HouseSize,Appliances,SellStatus,Price,Garage,Description,AdditionalInfo,Address,Location))
                managesCursor.execute('INSERT INTO Manages VALUES(?,?)',(HouseKey,realtorKey))

                conn.commit()
                conn.close()

                #redirect back ot the editing page
                return HttpResponseRedirect("EditHouse?h_housekey=" + str(HouseKey))
            except Exception as e:
                print(e)
                return HttpResponseRedirect("EditHouse?h_housekey=" + str(HouseKey))

        raise Http404("Not a Realtor")




def addPicture(request):
    if(request.method == 'GET'):
        HouseKey = 0
        if('h_housekey' in request.GET):
            HouseKey = request.GET.get('h_housekey')
        cont = {'HouseKey':HouseKey}
        return render(context=cont,request=request,template_name='uploadPic.html')

    elif(request.method == 'POST'):
        if('type' in request.session and request.session.get('type') == 'R'):
            conn = sqlite3.connect('RMHS.db')
            houseCursor = conn.cursor()
            picCursor = conn.cursor()
            realtorCursor = conn.cursor()

            try:
                HouseKey = request.POST.get('HouseKey',None)
                PictureURL = request.POST.get('PictureURL',None)

                #used to verify a realtor has permissions for this house
                realtorCursor.execute('SELECT distinct r_realtorKey FROM Realtor WHERE r_credentialKey = ?',(request.session.get('uname'),))
                realtorKey = realtorCursor.fetchone()[0]
                houseCursor.execute('SELECT h_housekey FROM House,Manages,Realtor WHERE h_housekey=? AND h_housekey=m_housekey AND m_realtor=?',(HouseKey,realtorKey))
                realtorOwnedHouseKey = houseCursor.fetchone()

                if(realtorOwnedHouseKey is not None):
                    #Since the realtor has edit permissions for this house, then we can edit it safely
                    picCursor.execute('SELECT max(p_pictureKey) FROM Pictures')
                    picKey = picCursor.fetchone()
                    if(picKey is None):
                        picKey = 0;
                    else:
                        picKey = int(picKey[0]) + 1
                    picCursor.execute('INSERT INTO Pictures VALUES(?,?,?)',(picKey,HouseKey,PictureURL))
                    conn.commit()
                    conn.close()

                #redirect back ot the editing page
                return HttpResponseRedirect("EditHouse?h_housekey=" + str(HouseKey))
            except Exception as e:
                print(e)
                return HttpResponseRedirect("EditHouse?h_housekey=" + str(HouseKey))
        raise Http404("Not a Realtor")


    raise Http404("Not a Realtor")
    
