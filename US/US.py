import json, requests, socket
from socket import *
from flask import Flask, request
from urllib.request import urlopen

app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])
def handle_request():
    # Parse the request
    hostname = request.args["hostname"]
    fs_port = request.args["fs_port"]
    number = request.args["number"]
    as_ip = request.args["as_ip"]
    as_port = request.args["as_port"]

    # Check if there is any missing parameter(s)
    if hostname == "" or fs_port == "" or number == "" or as_ip == "" or as_port == "":
        return '400: BAD REQUEST!'
    print("US SERVER: ")
    print("------------------------")
    print("hostname: "+hostname)
    print("fs_port: "+fs_port)
    print("number: "+number)
    print("as_ip: "+as_ip)
    print("as_port: "+as_port)
    print("------------------------")
    
    # Get the IP address of FS
    # Access FS, get Fibonacci number of X and status code
    as_ip_request = {"TYPE": "A","NAME": hostname}
    message = json.dumps(as_ip_request)
    print("Message: "+message)
    us_socket = socket(AF_INET, SOCK_DGRAM)
    print('Initialize socket successfully')
    as_port = int(as_port)
    print('Transferred as port number into Integer: '+str(as_port))
    us_socket.sendto(message.encode(), (as_ip, as_port))
    print('Send message to AS server successfully')
    response, server_address = us_socket.recvfrom(2048)
    decoded_response = response.decode()
    print('Receive message from AS: '+decoded_response)
    decoded_response_json = json.loads(decoded_response)
    fs_ip_address = decoded_response_json["VALUE"]
    print('FS IP RETRIEVED: '+fs_ip_address)
    url_link = 'http://' + fs_ip_address + ':' + fs_port + '/fibonacci?number=' + number
    print("URL: "+url_link)
    url_retrieve = urlopen(url_link)
    html_content = url_retrieve.read()
    print("Request URL successfully")
    print("HTML Content of page in FS Server: ")
    print(html_content)
    print("------------------------")
    print("------------------------")
    print("------------------------")
    return html_content


app.run(host='0.0.0.0',
        port=8080,
        debug=True)


                            