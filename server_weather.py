import socket
import json
import threading
import requests


base_url = "http://api.openweathermap.org/data/2.5/weather?"
api_key = '3cc8b948c77264abe15c6b003f1af9ca'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostbyname(socket.gethostname())
port = 10101

server_socket.bind((host, port))
print(f'Сервер запущен по адресу {host}, порту {port}')

server_socket.listen(5)


def handle_client(client_socket, client_address):
    print(f'Подключился клиент: {client_address}')
    message = 'Добро пожаловать! Вы подключены к серверу с погодой. ' \
              'Введите сообщение в виде "Страна, Город": '
    client_socket.send(message.encode())

    while True:
        client_message = client_socket.recv(1024).decode()

        if not client_message:
            print(f'Клиент {client_address} отключился')
            break


        city_name = input("Введите город: ")
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            answer = "Температура = " +\
                  str(current_temperature) +\
                  "\n Атмосферное давление = " +\
                  str(current_pressure) +\
                  "\n Влажность = " +\
                  str(current_humidity) +\
                  "\n Описание = " +\
                  str(weather_description)

        else:
            print("Город не найден")

        client_socket.send(answer.encode())

    client_socket.close()


while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()


