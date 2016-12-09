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
    uname = ""
    realtorKey = ""
    isRealtor = False
    if('type' in request.session and request.session.get('type') == 'R'):
        isRealtor = True
        uname = request.session.get('uname')

    if((request.method == 'GET' and 'r_realtorkey' in request.GET)):
        isRealtor = False
        realtorKey = (request.GET.get('r_realtorkey'),)

    if(len(realtorKey) > 0 or len(uname) > 0):
        listOfHouses = []
        conn = sqlite3.connect('RMHS.db')
        realtorCursor = conn.cursor()
        houseCursor = conn.cursor()
        picCursor = conn.cursor()

        if(isRealtor):
            realtorCursor.execute('SELECT distinct r_realtorKey FROM Realtor WHERE r_credentialKey = ?',(request.session.get('uname'),))
            (realtorKey) = realtorCursor.fetchone()
            if(realtorKey is None):
                return HttpResponseRedirect("../createAccount")

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

        realtorKey = realtorKey[0]

        print(len(listOfHouses))
        print(isRealtor)
        print(realtorKey)

        cont = {'realtorName':realtorKey,'house_list':listOfHouses,'isRealtor':isRealtor}
        return render(context=cont,request=request,template_name='realtorHouses.html')
    raise Http404("Not a Realtor")

def showRealtor(request):
    if(request.method == 'GET' and 'r_realtorkey' in request.GET):
        realtorKey = request.GET.get('r_realtorkey')
        conn = sqlite3.connect('RMHS.db')
        realtorCursor = conn.cursor()

        realtorCursor.execute('SELECT * FROM Realtor WHERE r_realtorKey = ?',(realtorKey,))
        realtor = realtorCursor.fetchone()
        if(realtor is not None):
            Description = realtor[2]
            Location = realtor[3]
            ContactInfo = realtor[5]

            realtorCursor.execute('SELECT avg(rv_rating) FROM Reviews WHERE rv_realtorkey=?',(realtorKey,))
            (avgRev) = realtorCursor.fetchone()
            print(avgRev)
            print("ha")
            if(avgRev is None):
                print(avgRev)
                avgRev = -1
            else:
                print(avgRev)
                avgRev = avgRev[0]
                if(avgRev is None):
                    avgRev = -1

            print(avgRev)

            conn.close()
            cont = {'RealtorKey':realtorKey,'Description':Description,'Location':Location,'ContactInfo':ContactInfo,'avgRev':avgRev}
            return render(context=cont,request=request,template_name='DisplayRealtor.html')

    return Http404("Invalid Realtor Key")

def allRealtors(request):
    listOfRealtors = []
    conn = sqlite3.connect('RMHS.db')
    realtorCursor = conn.cursor()

    for row in realtorCursor.execute('SELECT r_realtorKey FROM Realtor'):
        listOfRealtors.append(row[0])

    cont = {'realtor_list':listOfRealtors}
    return render(context=cont,request=request,template_name='realtors.html')




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
    

def createRealtor(request):
    if request.method == 'GET':
        if('type' in request.session and request.session.get('type') == 'R'):
            try:
                return render(request=request,template_name='createRealtor.html')
            except:
                raise Http404()
    elif request.method == 'POST':
        if('type' in request.session and request.session.get('type') == 'R'):
            conn = sqlite3.connect('RMHS.db')
            realtorCursor = conn.cursor()

            try:
                RealtorName = request.POST.get('RealtorName',None)
                CredentialKey = request.session.get('uname')
                RealtorName = request.POST.get('RealtorName')
                Description = request.POST.get('Description',None)
                Location = request.POST.get('Location',None)
                numSoldHouses = 0
                ContactInfo = request.POST.get('ContactInfo',None)

                if(RealtorName is None or len(RealtorName) == 0):
                    return HttpResponseRedirect("")

                realtorCursor.execute('SELECT * FROM Realtor WHERE r_realtorKey=? OR r_credentialKey=?',(RealtorName,CredentialKey))
                if(realtorCursor.fetchone() is not None):
                    #Realtor exists already
                    return Http404("<h6>User is already in charge of a realtor, or realtor name is taken, go back and try again</h6>")

                
                realtorCursor.execute('INSERT INTO Realtor VALUES(?,?,?,?,?,?)',(RealtorName,CredentialKey,Description,Location,numSoldHouses,ContactInfo))

                conn.commit()
                conn.close()

                #redirect back ot the editing page
                return HttpResponseRedirect("../Account")
            except Exception as e:
                print(e)
                return HttpResponse("<h6>Please go back and enter all data after having signed in as a realtor")

        raise Http404("Not a Realtor")

def review(request):
    if('uname' not in request.session):
        return Http404("Need to be logged in to write a review")
    if(request.method == 'GET' and 'r_realtorkey' in request.GET):
        cont = {'uname':request.session.get('uname'),'RealtorName':request.GET.get('r_realtorkey')}
        return render(context=cont,request=request,template_name='review.html')
    elif(request.method == 'POST'):
        
        try:
            Rating = int(request.POST.get('Rating',None))
            Comment = request.POST.get('Comment',None)
            RealtorKey = request.POST.get('RealtorKey',None)
            Reviewer = request.session.get('uname')


            conn = sqlite3.connect('RMHS.db')
            reviewCursor = conn.cursor()

            reviewCursor.execute('SELECT max(rv_reviewkey) FROM Reviews')
            (ReviewKey) = reviewCursor.fetchone()
            if(ReviewKey is None):
                ReviewKey = 0
            else:
                ReviewKey = ReviewKey[0] + 1

            print("hi")
            print(RealtorKey)

            reviewCursor.execute('INSERT INTO Reviews VALUES(?,?,?,?,?)',(ReviewKey,RealtorKey,Reviewer,Rating,Comment))
            conn.commit()
            conn.close()

            return HttpResponseRedirect("ShowRealtor?r_realtorkey=" + str(RealtorKey))

        except:
            return Http404("User entered data wrong, go back and try again")















