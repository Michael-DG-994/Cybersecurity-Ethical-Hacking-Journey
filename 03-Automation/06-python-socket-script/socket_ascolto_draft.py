
#Socket di ascolto

import socket
SVR_ADDR = "192.168.50.100"
SVR_PORT = 44444

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((SVR_ADDR,SVR_PORT))

s.listen(1)
print("Server started! Wauting for connection...")

connection, address = s.accept()
print(f"Client connected with address: {address}")

while 1:
    data = connection.recv(1024)

    if not data:
        break

    connection.sendall(b"-- Message Received --\n")
    print(data.decdode('utf-8'))

connection.close()