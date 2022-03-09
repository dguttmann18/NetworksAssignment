from audioop import add
from getpass import getuser
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

def getAddress(userName):
    i = 0

    while usernames[i] != userName and i < len(usernames):
        i += 1
    
    if (usernames[i] == userName):
        return addresses[i]
    else:
        return NULL

def getUsername(address):
    i = 0

    while addresses[i] != address and i < len(addresses):
        i += 1
    
    if (addresses[i] == address):
        return usernames[i]
    else:
        return NULL

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

        print("User connected")

        if username in usernames:
            msgFromServer = "REJECT"
            bytesToSend = str.encode(msgFromServer)
            UDPServerSocket.sendto(bytesToSend, address)
        else:
            usernames.append(username)
            addresses.append(address)
            users = ""

            for u in usernames:
                users += u + "#"

            users = users[:-1]
            msgFromServer = "ACCEPT|"  + users

            bytesToSend = str.encode(msgFromServer)
            UDPServerSocket.sendto(bytesToSend, address)

            for a in addresses:
                if a != address:
                    msgFromServer = "ADD|" + username
                    bytesToSend = str.encode(msgFromServer)
                    UDPServerSocket.sendto(bytesToSend, a)
    elif command == "CHAT":
        receiver = clientMsg[1]
        receiverAddress = getAddress(receiver)
        dataToSend = "CHAT|" + getUsername(address) + "|" + clientMsg[2]
        bytesToSend = str.encode(dataToSend)
        UDPServerSocket.sendto(bytesToSend, receiverAddress)
    elif command == "CHECK": #######
        receiver = clientMsg[1]
        receiverAddress = getAddress(receiver)
        dataToSend = "CHECK|" + getUsername(address) + "|" + clientMsg[2]
        bytesToSend = str.encode(dataToSend)
        UDPServerSocket.sendto(bytesToSend, receiverAddress)


    '''
    for i in range(len(addresses)):
        for j in range(len(usernames)):
            print("Inside here")
            msgFromServer = "ADD|" + usernames[j]
            bytesToSend = str.encode(msgFromServer)
            UDPServerSocket.sendto(bytesToSend, addresses[i])
            print("Sent")
    '''
