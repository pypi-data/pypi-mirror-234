import socket


def check(url):
    filename = url[7:]
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(filename)
        return True
    except Exception:
        return False
