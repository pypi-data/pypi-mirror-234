from numpy import radians,degrees,sqrt,sin,cos,tan,arctan,arctan2
from pycegm import units

def llh_to_xyz(phi,lamda,h,a,b):
    '''
    Function to convert lat,lon coordinate to cartesian XYZ

        * Args:
        ----
            - phi : latitude in degree,minute,seconds,direction [dictionary]
            - lambda : longitude in degree,minute,seconds,direction [dictionary]
            - lat : height in m
            - a : semi-major axis ellipsoid
            - b : semi-minor axis ellipsoid
        
        * Returns:
        ----
                - x,y,z
    '''
    # convert to degree decimal
    phi_decimal = units.dms_to_decimal(phi)
    lamda_decimal = units.dms_to_decimal(lamda)

    # we convert to radians
    phi = radians(phi_decimal)
    lamda = radians(lamda_decimal)

    e_2 = (a**2-b**2)/a**2

    nu = a/sqrt(1-e_2*sin(phi)**2)

    X = (nu + h)*cos(phi)*cos(lamda)
    Y = (nu + h)*cos(phi)*sin(lamda)
    Z = (nu*(1-e_2) + h)*sin(phi)
    
    return X,Y,Z

def xyz_to_llh(X,Y,Z,a,b,dms=True):
    '''
    Function to convert Cartesian X,Y,Z coordinates to Ellipsoidal

        * Args:
        ----
            - X :
            - Y :
            - Z :
            - a :
            - b :
        * Returns:
        ----
            lat:
            lon:

    '''
    e_2 = (a**2-b**2)/a**2
    epsilon = e_2/(1-e_2)
    p = sqrt(X**2+Y**2)
    u = arctan((Z*a)/(p*b))

    phi = arctan( (Z+epsilon*b*sin(u)**3)  /  (p-e_2*a*cos(u)**3)  )
    lamda = arctan2(Y,X)

    nu = a/sqrt(1-e_2*sin(phi)**2)

    h = (X/(cos(phi)*cos(lamda)))-nu

    phi_decimal = degrees(phi)
    lamda_decimal = degrees(lamda)

    if (dms):
        # latitude
        phi_degrees,phi_minutes,phi_seconds,phi_direction = units.decimal_to_dms(phi_decimal,
                                                                             "latitude")
        # longitude
        lamda_degrees,lamda_minutes,lamda_seconds,lamda_direction = units.decimal_to_dms(lamda_decimal,"longitude")
        lat = {"deg":phi_degrees,
            "min":phi_minutes,
            "sec":phi_seconds,
            "dir":phi_direction
            }
        lon = {"deg":lamda_degrees,
            "min":lamda_minutes,
            "sec":lamda_seconds,
            "dir":lamda_direction
            }
        return lat,lon,h
    else:
        return phi_decimal,lamda_decimal,h

