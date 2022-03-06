from ipaddress import ip_address
from re import U
import socket
import sys

localIP     = "127.0.0.1"
localPort   = 20007
bufferSize  = 1024
hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)

usernames = []
addresses = []

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind to address and ip
UDPServerSocket.bind((IP, localPort))

print("UDP server up and listening")

msgNum = 0

# Listen for incoming datagrams
while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    clientMsg = message.decode().split("|")
    clientIP  = "Client IP Address:{}".format(address)

    command = clientMsg[0]

    if command == "JOIN":
        username = clientMsg[1]

        if username in usernames:
            msgFromServer = "REJECT"
        else:
            usernames.append(username)
            addresses.append(address)
            users = ""

            for u in usernames:
                users += u + "#"

            users = users[:-1]
            msgFromServer = "ACCEPT|"  + users

    
    '''
    comp = clientMsg.split("#")
    nme = comp[0]
    msg = comp[1]

    print(nme + ": " + msg)
    print(clientIP)
    '''
    msgNum += 1
    bytesToSend = str.encode(msgFromServer)

    # Sending a reply to client
    UDPServerSocket.sendto(bytesToSend, address)

    for i in range(len(usernames)):
        print("Inside here")
        msgFromServer = "ADD|" + usernames[i]
        bytesToSend = str.encode(msgFromServer)
        UDPServerSocket.sendto(bytesToSend, addresses[i])

'''
sPort = 20000
sSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
sSocket.bind(('', sPort))
print("Server ready")

while True:
    message, cAddress = sSocket.recvfrom(2048)
    modifiedMessage = message.decode().upper()
    sSocket.sendto(modifiedMessage.endode(), cAddress)
'''