from socket import *
import json

server_port = 53533

as_socket = socket(AF_INET, SOCK_DGRAM)
as_socket.bind(('', server_port))

dns_record_dictionary = {}

# Need to keep track of any messages received from socket
while True:
    sender_message, sender_address = as_socket.recvfrom(2048)

    # Check whether FS or US send the message to socket
    decoded_message = json.loads(sender_message.decode())
    print("AS SERVER:")
    print("------------------------")
    print("Decoded message: ")
    print(decoded_message)

    # For FS request, there are 4 keys: Name, Value, Type, TTL
    # For US request, there are 2 keys: Name, Type
    # Here we use the number of keys in the message to identify whether it
    # is from FS / US
    number_of_keys = len(decoded_message)
    print('Number of keys: '+str(number_of_keys))
    print("------------------------")

    response_message = ''.encode()

    # Function 1: Registration of DNS Record (FS request)
    if number_of_keys == 4:
        print("Function 1: Registration of DNS Record (FS request)")
        hostname = decoded_message["NAME"]
        ip = decoded_message["VALUE"]
        type = decoded_message["TYPE"]
        ttl = decoded_message["TTL"]
        print("NAME: "+hostname)
        print("VALUE: " +ip)
        print("TYPE: "+type)
        print("TTL: "+str(ttl))

        key = hostname + '-' + type
        dns_record = {"TYPE": type, "NAME": hostname, "VALUE": ip, "TTL": ttl}
        print("Key: "+key)
        print("DNS Record: ")
        print(dns_record)
        dns_record_dictionary[key] = dns_record
        print("WHOLE DNS RECORD DICTIONARY:")
        print(dns_record_dictionary)
        content = 'Successfully registered'
        response_message = json.dumps(content).encode()

    # Function 2: DNS Query (US Request)
    else:
        print("Function 2: DNS Query (US Request)")
        hostname = decoded_message["NAME"]
        type = decoded_message["TYPE"]
        print("NAME: "+hostname)
        print("TYPE:" +type)
        
        key = hostname + '-' + type
        dns_record = dns_record_dictionary[hostname + '-' + type]
        print("Key: "+key)
        print("DNS Record: ")
        print(dns_record)
        fs_ip = dns_record["VALUE"]
        print("---> FS IP : "+fs_ip)
        content = json.dumps(dns_record)
        response_message = str(content).encode()

    # Send back response message using socket
    as_socket.sendto(response_message, sender_address)
    print("Reponse sent!")
    print("------------------------")
    print("------------------------")
    print("------------------------")


