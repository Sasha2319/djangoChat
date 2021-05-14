import socket

user = {}
allchats = []

def get_ip(request):
    ip = ''
    pc = socket.gethostname()
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')  ### Real IP address of client Machine
    return ip, pc