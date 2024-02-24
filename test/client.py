import socket
import json
c = socket.socket()
c.connect(('192.168.210.179',9999))

city=input("Enter city:")

c.send(bytes(city,'utf-8'))

rec_data=c.recv(1024).decode()
weather_data=json.loads(rec_data)

if weather_data['error']==0:
    temperature=weather_data['temperature']
    description=weather_data['description']
    humidity=weather_data['humidity']
    wind_speed=weather_data['wind speed']
    print('Temperature:',temperature,'°C')
    print('Description:',description)
    print('Humidity',humidity,'%')
    print('Wind Speed',wind_speed,'m/s')
else:
    status_code=weather_data['status_code']
    print(f'Error fetching data for {city}. Status code: {status_code}')

c.close()
