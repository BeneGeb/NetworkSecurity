import socket
from dnslib import DNSRecord
import base64
import sys


def parse_dns_response(data):
    dns_request = DNSRecord.parse(data)
    domain = str(dns_request.q.qname).rstrip('.')

    return domain

if __name__ == '__main__':
    received_data = ""

    port = 53
    ip = sys.argv[1]

    print(f"Server running on {ip}:{port}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))

    while True:
        data, addr = sock.recvfrom(512)
        r = parse_dns_response(data)

        received_data += r

        if r[-1] == "=":
            received_bytes = received_data.encode('utf-8')
            b64decoded = base64.b64decode(received_bytes)
            print(b64decoded.decode('utf-8'))
    