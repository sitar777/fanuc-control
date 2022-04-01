import socket

from src.config import settings

# ZTESTSEM2

# 1 100 100 100 100 100 100 150 1
# To point 0.1 0.1 0.1 0.1 0.1 0.1 with velocity 150 mm/sec
# ? X Y Z W P R Velocity ?

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((settings.FANUC_HOST, settings.FANUC_PORT))
    print("Socket connected")

    s.sendall(b'600000 200000 600000 -180000 30000 0 300 1')
    data = s.recv(1024)

    print(data)
