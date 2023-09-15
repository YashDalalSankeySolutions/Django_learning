from django.shortcuts import render
from django.http import JsonResponse
from .validation import bookingFieldCheck,checkId,checkEmail,checkName,checkNumber
from random import randint
from .models import booking
import json
import requests
# Create your views here.

def book_trip(request):

    data = json.loads(request.body)
    if(request.method!='POST' or (not bookingFieldCheck(data))):
        return JsonResponse({"message":"bad Request"},status= 400) 
    
    try:
        if(checkId(data["trip_id"],"tripId") and checkId(data["user_id"],"userId") and checkName(data["traveller_name"]) and checkNumber(data["traveller_number"]) and type(data["ticket_cost"])==int and checkEmail(data["traveller_email"])):
            
            ticket_ID = "TK"+str(randint(10000000,99999999))
            # check ticketId Existence
            while(booking.objects.filter(ticket_id=ticket_ID)):
               ticket_ID = "TK"+str(randint(10000000,99999999))

            # # check user already booked a trip
            # if(booking.objects.filter(traveller_number=data["traveller_number"]) or booking.objects.filter(traveller_email=data["traveller_email"])):
            #     return JsonResponse({"message":"User has already book the trip"},status=400)
            
            # check trip Existence
            getTripListUrl = "http://127.0.0.1:8000/trip/details"
            payload={
                "trip_id":data["trip_id"]
                # "trip_id":""
            }
            payload = json.dumps(payload)
            res = requests.post(getTripListUrl,headers={'Content-Type': 'application/json'},data=payload)
            
            if(res.status_code==404):
                return JsonResponse(json.loads(res.text),status=404)
            elif(res.status_code==200):
                bookingObject = booking()
                bookingObject.ticket_id = ticket_ID
                bookingObject.trip_id = data["trip_id"]
                bookingObject.user_id = data["user_id"]
                bookingObject.traveller_name = data["traveller_name"]
                bookingObject.traveller_number = data["traveller_number"]
                bookingObject.ticket_cost = data["ticket_cost"]
                bookingObject.traveller_email = data["traveller_email"]
                bookingObject.save()
                return JsonResponse({"message":"Trip Booked Successfully"},status=200)
            else:
                raise Exception(json.loads(res.text)["message"])
               
        else:
            raise Exception("Invalid DataFields")

    except Exception as e:
        return JsonResponse({"message":str(e)},status=500)
    

def bookingList(request):
    data=json.loads(request.body)
    if(request.method!='POST' or (not "user_id" in data.keys())):
        return JsonResponse({"message":"bad Request"},status= 400)
    
    try:
        sortBy = data["sort_by"] if ("sort_by" in data.keys() and data["sort_by"]!="") else "ticket_cost"
        order = data["order"] if ("order" in data.keys()and data["order"]!="") else "asc"
        pageNo = data["page_no"] if ("page_no" in data.keys()and data["page_no"]!="" and data["page_no"]>0) else 1
        no_of_data_in_page = 2
        
        # check valid userId
        if(not checkId(data["user_id"],"userId")):
            raise Exception("Invalid userId")
        
        booking_list = booking.objects.filter(user_id=data["user_id"]).order_by("-"+sortBy).values()
    
        if(order=='desc'):
            booking_list = booking_list.reverse()

        booking_list = json.dumps(list(booking_list))
        booking_list = json.loads(booking_list)

        starting_index = (pageNo-1)*no_of_data_in_page
        if(starting_index>=len(booking_list)):
            return JsonResponse({"message":"No Data for this Page"},status=404)
        last_index = (pageNo*no_of_data_in_page) if (pageNo*no_of_data_in_page) < len(booking_list) else len(booking_list)

        booking_list = booking_list[starting_index:last_index]
        return JsonResponse({"page":pageNo,"BookingList":booking_list},status=200)
    
    except Exception as e:
        return JsonResponse({"message":str(e)},status=500)
    

def BookingDetails(request):
    data=json.loads(request.body)
    if(request.method!='POST' or (not "ticket_id" in data.keys())):
        return JsonResponse({"message":"bad Request"},status= 400)
    
    try:
        # check valid ticket Id
        if(not checkId(data["ticket_id"],"ticketId")):
            raise Exception("Invalid Ticket ID")
        
        # check booking Existence
        # print("----------")
        booking_res = booking.objects.filter(ticket_id=data["ticket_id"])
        # print("----------",booking_res)
        if(booking_res.count()==0):
            raise Exception("Booking Not Exist")
        
        booking_list = booking_res.values()
        booking_list = booking_list[0]

        getTripListUrl = "http://127.0.0.1:8000/trip/details"
        payload={
            "trip_id":booking_list["trip_id"]
            # "trip_id":""
        }
        payload = json.dumps(payload)
        trip_res = requests.post(getTripListUrl,headers={'Content-Type': 'application/json'},data=payload)
        # print("trip_res--------->",trip_res)

        if(trip_res.status_code==404):
            return JsonResponse(json.loads(trip_res.text),status=404)
        
        elif(trip_res.status_code==200):
            trip_details = json.loads(trip_res.text)["TripDetails"]
            booking_list["trip_details"] = trip_details

        else:
            raise Exception(json.loads(trip_res.text)["message"])
        
        return JsonResponse({"BookingDetails":booking_list})
    
    except Exception as e:
        status=500
        if(str(e)=="Booking Not Exist"):
           status= 404
        return JsonResponse({"message":str(e)},status=status)    