import re
def bookingFieldCheck(data):
    s1 = set(["trip_id","traveller_name","traveller_number","ticket_cost","traveller_email"])
    return s1.issubset(data.keys())

def checkId(id,field):
    if(len(id)!=10):
        return False
        
    if(field == 'ticketId' and re.search("^TK[0-9]{8}$",id)):
        return True
    elif(field == 'tripId' and re.search("^TP[0-9]{8}$",id)):
        return True
    elif(field == 'userId' and re.search("^UD[0-9]{8}$",id)):
        return True
    else:
        return False
    
def checkName(name):
    if(type(name)==str and re.search("^[a-zA-Z ]+$",name)):
        return True
    else: 
        return False
    
def checkEmail(email):
    if(type(email)==str and re.search("^[a-zA-Z0-9\.]+@[a-zA-Z]+?\.[a-zA-Z]{2,3}$",email)):
        return True
    else: 
        return False
    
def checkNumber(number):
    print("----------",number)
    if(type(number)==int and re.search("^9[0-9]{9}$",str(number))):
        return True
    return False
