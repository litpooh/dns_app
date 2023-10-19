import json, requests
import socket
from flask import Flask, request
from socket import *

app = Flask(__name__)

def calculte_fibonacci_number(input_number):
    number = int(input_number)
    # F(0) = 1
    # F(1) = 1
    # F(n) = F(n-1) + F(n-2)
    if number == 1:
        return 1
    elif number == 2:
        return 1
    else:
        return calculte_fibonacci_number(number - 1) + calculte_fibonacci_number(number - 2)

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

# Function 4: Fibonacci number for X
@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    # Check type is int
    number = request.args['number']
    if is_integer(number):
        return '200 OK. The Fibonacci number of '+str(number)+' is '+str(calculte_fibonacci_number(number))
    else:
        return '400: BAD FORMAT!'


# Function 1: Hostname Specification
# Function 2: Registration to Authoritative Server
# Function 3: Return 201 for Successful Resgistration
@app.route('/register', methods=['PUT'])
def register():
    information = request.get_json()
    hostname = information.get("hostname")
    ip = information.get("ip")
    as_ip = information.get("as_ip")
    as_port = information.get("as_port")
    print("FS SERVER:")
    print("------------------------")
    print("hostname: "+hostname)
    print("ip: "+ip)
    print("as_ip: "+as_ip)
    print("as_port: "+as_port)
    print("------------------------")

    form_dns_message = {"TYPE": "A","NAME": hostname,"VALUE": ip,"TTL": 10}
    print('Form DNS message successfully!')

    dns_message = json.dumps(form_dns_message)
    print('Form DNS JSON message successfully:'+dns_message)

    as_port = int(as_port)
    print('Transferred as port number into Integer: '+str(as_port))
    fs_socket = socket(AF_INET, SOCK_DGRAM) 
    print('Initialize socket successfully')
    fs_socket.sendto(dns_message.encode(), (as_ip, as_port))
    print('Send message to AS server successfully')
    received_message, server_address = fs_socket.recvfrom(2048)
    print('Receive message from AS: '+received_message.decode())
    fs_socket.close()
    print("------------------------")
    print("------------------------")
    print("------------------------")
    return '201'


app.run(host='0.0.0.0',
        port=9090,
        debug=True)
    






