import os

def flip(box):
    return(box[0],box[3],box[2],box[1])

def get_domain(center, dims, trim=False):

    lon = center[0]
    lat = center[1]
    xradius = dims[0] / 2.0
    yradius = dims[1] / 2.0

    lat1 = lat - yradius
    lon1 = lon - xradius

    lat2 = lat + yradius
    lon2 = lon + xradius
        
    if lon1 < -180.0:
        lon1 += 360.0
        lon2 = lon1 + xradius*2
            
    if lon2 > 360.0:
        lon2 -= 360.0
        lon1 = lon2 - xradius*2

    if trim:
        return(round(lon1), round(lat1), round(lon2), round(lat2))

    return (lon1, lat1, lon2, lat2)

def strdirtime(time_dt, pathname):

    if not pathname:
        return pathname

    path = os.path.dirname(pathname)
    name = os.path.basename(pathname)

    path = time_dt.strftime(path)
    return os.path.join(path, name)

def strf2time(format, time1, time2=None):

    while True:
        index = format.find('%%')
        if index == -1:
            break

        token = format[index:index+3]
        value = time1.strftime(token[1:])
        format = format.replace(token, value)

    if time2:
        format = time2.strftime(format)

    return format
