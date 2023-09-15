import re

def tripFieldsCheck(data):
    s1 = set(["user_id","vehicle_id","route_id","driver_name","trip_distance"])
    return s1.issubset(data.keys())


def checkId(id,field):
    
    if(len(id)!=10):
        return False
        
    if(field == 'userId' and re.search("^UD[0-9]{8}",id)):
        return True
    elif(field == 'vehicleId' and re.search("^VD[0-9]{8}",id)):
        return True
    elif(field == 'routeId' and re.search("^RT[0-9]{8}",id)):
        return True
    elif(field == 'tripId' and re.search("^TP[0-9]{8}",id)):
        return True
    else:
        return False

def checkName(name):
    if(type(name)==str and re.search("^[a-zA-Z ]+$",name)):
        return True
    else: 
        return False
    

    