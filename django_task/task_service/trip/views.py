from django.shortcuts import render
from django.http import JsonResponse
import json
from random import randint
from .models import trips
from route.models import route
from .validation import checkId,checkName,tripFieldsCheck
from django.core import serializers
from django.db.models import F

# Create your views here. 
def add_trip(request):
    data = json.loads(request.body)
    try:
        if(request.method!='POST' or (not tripFieldsCheck(data))):
           return JsonResponse({"message":"bad Request"},status= 400)
        if(checkId(data["user_id"],"userId") and checkId(data["vehicle_id"],"vehicleId") and checkId(data["route_id"],"routeId") and checkName(data["driver_name"]) and type(data["trip_distance"])==int):
            
            trip_ID = "TP"+str(randint(10000000,99999999))

            # check tripId Existence
            while(trips.objects.filter(trip_id=trip_ID)):
               trip_ID = "TP"+str(randint(10000000,99999999))

            # check route Existence
            if(route.objects.filter(route_id=data["route_id"]).count()==0):
                raise Exception("Route Not Exist")
            
            tripsObject = trips()
            tripsObject.trip_id=trip_ID
            tripsObject.user_id=data["user_id"]
            tripsObject.vehicle_id=data["vehicle_id"]
            tripsObject.route_id=route.objects.get(route_id=data["route_id"])
            tripsObject.driver_name=data["driver_name"].strip()
            tripsObject.trip_distance=data["trip_distance"]
            tripsObject.save()
            
            return JsonResponse({"message":"Trip Added Successfully"},status=200)
        
        else: 
            raise Exception("Invalid DataFields")

    except Exception as e:
        return JsonResponse({"message":str(e)},status=500)
    
def trip_list(request): 
    data=json.loads(request.body)
    if(request.method!='POST' or (not "user_id" in data.keys())):
        return JsonResponse({"message":"bad Request"},status= 400)
    
    try:
        sortBy = data["sort_by"] if ("sort_by" in data.keys() and data["sort_by"]!="") else "trip_id"
        order = data["order"] if ("order" in data.keys()and data["order"]!="") else "asc"
        pageNo = data["page_no"] if ("page_no" in data.keys()and data["page_no"]!="" and data["page_no"]>0) else 1
        no_of_data_in_page = 2
        # check valid userId
        if(not checkId(data["user_id"],"userId")):
            raise Exception("Invalid userId")
        
        trip_list = trips.objects.filter(user_id=data["user_id"]).order_by(sortBy).values()
        
        if(order=='desc'):
            trip_list = trip_list.reverse()

        trip_list = json.dumps(list(trip_list))
        trip_list = json.loads(trip_list)


        starting_index = (pageNo-1)*no_of_data_in_page
        if(starting_index>=len(trip_list)):
            return JsonResponse({"message":"No Data for this Page"},status=404)
        last_index = (pageNo*no_of_data_in_page) if (pageNo*no_of_data_in_page) < len(trip_list) else len(trip_list)
        trip_list = trip_list[starting_index:last_index]

        return JsonResponse({"page":pageNo,"TripList":trip_list},status=200)
    
    except Exception as e:
        return JsonResponse({"message":str(e)},status=500)
    

def trip_details(request):
    data=json.loads(request.body)
    if(request.method!='POST' or (not "trip_id" in data.keys())):
        return JsonResponse({"message":"bad Request"},status= 400)
    
   
    try:
        # check valid trip Id
        if(not checkId(data["trip_id"],"tripId")):
            raise Exception("Invalid Trip ID")
        
        # check trip Existence
        trip_res = trips.objects.filter(trip_id=data["trip_id"]).annotate(
            route_id_ = F('route_id_id__route_id'),
            route_name = F('route_id_id__route_name'),
            route_origin = F('route_id_id__route_origin'),
            route_destination = F('route_id_id__route_destination'),
            route_stops = F('route_id_id__stops'),
        ).values(
            'trip_id',
            'user_id',
            'vehicle_id',
            'driver_name',
            'trip_distance',
            'route_id_',
            'route_name',
            'route_origin',
            'route_destination',
            'route_stops'
        )
        if(not trip_res):
            raise Exception("Trip Not Exist")
        trip_res = trip_res[0]
        
        return JsonResponse({"TripDetails":trip_res})     
    except Exception as e:
        status=500
        if(str(e)=="Trip Not Exist"):
            status= 404
        return JsonResponse({"message":str(e)},status=status)
    