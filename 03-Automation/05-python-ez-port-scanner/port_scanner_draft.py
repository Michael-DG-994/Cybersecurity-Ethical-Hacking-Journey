
#scanner semplice di porte aperte

import socket

target = input("Insert the IP address you would like to scan: ")
port_range = input("Insert the RANGE of ports you want to scan (ex. 1-666): ")

lowport = int(port_range.split("-")[0])
highport = int(port_range.split("-")[1])

print(f"Now scanning '{target}' from port '{lowport}' to '{highport}'...")

closed_port=[]

for port in range(lowport, highport+1):
    s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    status = s.connect_ex((target, port))
    if (status == 0):
      print(f"***Port: {port} is open***")
    else:
       closed_port.append(port)
    
print(f"There are {len(closed_port)} closed ports.")

    
