import socket

from src.config import settings


def send_message(msg: bytes):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((settings.FANUC_HOST, settings.FANUC_PORT))
        s.sendall(msg)
        data = s.recv(1024)
    return data.decode()
