import socket


def get_ip() -> str:
    """Get current IP"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
    except TimeoutError:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip
