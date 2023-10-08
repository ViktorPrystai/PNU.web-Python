import socket


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server_address = ('127.0.0.1', 12345)
client_socket.connect(server_address)

while True:
    message = input("Введіть текст для відправки на сервер (або 'exit' для виходу): ")
    if message.lower() == 'exit':
        break

    
    client_socket.send(message.encode('utf-8'))


client_socket.close()
