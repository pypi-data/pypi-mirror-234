from math import cos,sin,tan,asin,atan,atan2,radians,degrees,floor,sqrt

def dms_to_decimal(dms):
    '''
    Functions to convert latitude/longitude from degrees,minutes,seconds
    to decimal degrees
    
        * Args:
        ----
        deg : degrees
        min : minutes
        sec : seconds
        dir : direction, "N" or "S" for latitude; "E" or "W" for longitude [string]
              None is used for no direction 
        
        * Returns:
        dec : decimal degree
    '''
    deg = dms['deg']
    min = dms['min']
    sec = dms['sec']
    dir = dms['dir']

    dec = float(deg) + float(min)/60 + float(sec)/3600
    
    if (dir=="N" or dir=="E" or dir==None):
        dec*=1
    elif (dir=="S" or dir=="W"):
        dec*=-1
    else:
        print("direction symbol not recognized!!")
        return -1
    
    return dec


def decimal_to_dms(dec,comp):
    '''
    Functions to convert latitude/longitude decimal degrees to degrees,minutes,seconds
    
        * Args:
        ----
        dec : decimal degree
        comp : "latitude" or "longitude"
        
        * Returns:
        deg : degrees
        min : minutes
        sec : seconds
        dir : direction, "N" or "S" for latitude; "E" or "W" for longitude [string]
        
    '''
    south = False
    west = False
    
    if(dec < 0 and comp=="latitude"): 
        dec*=-1
        south = True
    if(dec < 0 and comp=="longitude"): 
        dec*=-1
        west = True
    
    deg = floor(dec)
    min = floor((dec - deg) * 60)
    sec = dec*3600 - deg*3600 - min*60
    
    if (comp=="latitude"):
        if south:
            dir = 'S'
        else: 
            dir = 'N'
    elif (comp=="longitude"):
        if west:
            dir = 'W'
        else:
            dir = 'E'
    
    return deg,min,sec,dir

