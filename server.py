from socket import *
import datetime
import calendar
import time


def date_today():
    date_time = str(datetime.datetime.today())
    my_date = datetime.datetime.today()
    week_day = str(calendar.day_name[my_date.weekday()])
    message =  date_time+';'+week_day
    return message

serverSocket = socket(AF_INET, SOCK_DGRAM) # IPv4 + UDP
serverSocket.bind(('127.0.0.2', 5555))
print("...The server is ready...")
msg = date_today()
while True:
    _,clientAddress = serverSocket.recvfrom(2048)
    serverSocket.sendto(msg.encode("utf-8"), clientAddress)
    time.sleep(5)