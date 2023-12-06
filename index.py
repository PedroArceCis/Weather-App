from datetime import date
from flask import Flask,render_template, request
from socket import *
import requests

app = Flask(__name__)

def order_message(message):
    result = []
    message = message.split(';')
    result.append(message[1])
    message = message[0].split(' ')
    result.append(message[0])
    result.append(message[1])
    return result

    
@app.route('/')
def index():
    return render_template('temperature.html')

    
@app.route('/', methods=['POST'])
def temperature():
    direction = request.form['search']
    direction = direction.strip()
    response_dir = requests.get("http://api.positionstack.com/v1/forward?access_key=dab23ab1125a14e93748084beeb83a49&query="+direction+"&limit=1")
    coor = (response_dir.json()["data"][0]["latitude"],response_dir.json()["data"][0]["longitude"])
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?lat='+str(coor[0])+'&lon='+str(coor[1])+'&appid=554c739a464db58f27114171ced4c066&units=metric')
    json_object = {
        'details temp':r.json()["main"],
        'sky status':r.json()["weather"][0]["description"]
    }
    temp_k = json_object['details temp']['temp']
    temp_min = json_object['details temp']['temp_min']
    temp_max = json_object['details temp']['temp_max']
    try:
       clientSocket = socket(AF_INET, SOCK_DGRAM) 
       message = 'ready to receive'
       clientSocket.sendto(message.encode("utf-8"),('127.0.0.2', 5555))
       modifiedMessage, _ = clientSocket.recvfrom(2048)
       date_data = modifiedMessage.decode()
       date_data = order_message(date_data)
       fecha = date_data[1]
       hora = 'Consultado a las: '+date_data[2][:5]+' horas'
       week_day = date_data[0]
    except:
        fecha =''
        hora = ''
        week_day = ''
        date_data = ['','','']
    return render_template('temperature.html', temp=str(temp_k)+'°c', direction=direction, min_temp='minima '+str(temp_min)+'°c', max_temp='maxima '+str(temp_max)+'°c',details=week_day, date=fecha, hour= hora)




if __name__ == "__main__":
    app.run( debug = True)