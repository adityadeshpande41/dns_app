import socket

UDP_PORT = 53533
DNS_DB = {}

def save_dns_record(name, value):
    DNS_DB[name] = value

def query_dns_record(name):
    return DNS_DB.get(name, None)

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('0.0.0.0', UDP_PORT))

while True:
    data, addr = udp_socket.recvfrom(1024)
    message = data.decode()
    lines = message.split('\n')

    if lines[0] == "TYPE=A" and "NAME=" in lines[1] and "VALUE=" in lines[2]:
        name = lines[1].split('=')[1]
        value = lines[2].split('=')[1]
        save_dns_record(name, value)

    elif lines[0] == "TYPE=A" and "NAME=" in lines[1]:
        name = lines[1].split('=')[1]
        response = query_dns_record(name)
        if response:
            reply = f"TYPE=A\nNAME={name}\nVALUE={response}\nTTL=10"
            udp_socket.sendto(reply.encode(), addr)

udp_socket.close()
