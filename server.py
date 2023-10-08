import socket
import datetime


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server_address = ('127.0.0.1', 12345)
server_socket.bind(server_address)


server_socket.listen(1)
print("Сервер працює на {}:{}".format(*server_address))

while True:
    print("Чекаємо на з'єднання...")
    client_socket, client_address = server_socket.accept()
    print("З'єднання встановлено з {}".format(client_address))

    data = client_socket.recv(1024).decode('utf-8')
    if not data:
        break

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Отримано від клієнта: '{}'".format(data))
    print("Час отримання: {}".format(current_time))

    client_socket.close()


server_socket.close()
