import sys
import datetime as dt

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

time1 = dt.datetime(2025,1,1,0)
time2 = dt.datetime(2025,1,5,12)

print(strf2time(sys.argv[1], time1, time2))
