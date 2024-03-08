import dnslib
import base64
import socket
import sys
import hashlib

def send_dns_query(data, server_ip, server_port=53):
    dns_request = dnslib.DNSRecord.question(data)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(5) 
        sock.sendto(dns_request.pack(), (server_ip, server_port))
  
        try:
            data, _ = sock.recvfrom(1024)
            dns_response = dnslib.DNSRecord.parse(data)

            received_data = str(dns_response.rr[0].rname)
            splitted_received_data = received_data[:-5]
       
            return splitted_received_data
           
        except socket.timeout:
            print("Die DNS-Anfrage hat ein Timeout erreicht.")
            return None


def decode_response(response):
    str_reponse = ""
    for r in response:
        str_reponse += r

    return base64.b64decode(str_reponse).decode()

def split_bytes(data, chunk_size):
    splitted_data = []
    for i in range(0, len(data), chunk_size):
        splitted_data.append(data[i:i+chunk_size])

    return splitted_data

def gen_hash(payload): 
    md5_hash = hashlib.md5()
    md5_hash.update(payload.encode())
    result = md5_hash.hexdigest()
    return result


if __name__ == '__main__':
    server_addr = sys.argv[1]
    filename = sys.argv[2]

    fragment_count = send_dns_query(f"{filename}.com", server_addr)
    fragment_count = int(fragment_count)
    
    response = []
    for i in range(fragment_count):
        curr_response = send_dns_query(f"{i}.{filename}.com", server_addr)
        response.append(curr_response.split("'")[1])

    decoded_string = decode_response(response)

    received_md5 = send_dns_query(f"{fragment_count+1}.{filename}.com", server_addr)
    hsh = gen_hash(decoded_string)
    
    if hsh == received_md5:
        print(decoded_string)
    else:
        print("Error in extracting Data")



    


    