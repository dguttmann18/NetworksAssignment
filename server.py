from audioop import add
from getpass import getuser
from ipaddress import ip_address
from pydoc import cli
from re import U
import socket
import sys


'''
Declare global variables and assign default values.
'''
localIP     = "127.0.0.1"
localPort   = 20007
bufferSize  = 1024
hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)

usernames = []
addresses = []

'''
This methods returns the address of the parsed username.
'''
def getAddress(userName):
    i = 0

    while usernames[i] != userName and i < len(usernames):
        i += 1
    
    if (usernames[i] == userName):
        return addresses[i]
    else:
        return NULL

'''
This method returns the username currently associated with the parsed address
'''
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

        print(username + "connected")

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
        msgNum = clientMsg[2]
        checkSum = clientMsg[3]
        data = clientMsg[4]

        receiverAddress = getAddress(receiver)
        dataToSend = "CHAT|" + getUsername(address) + "|" + msgNum + "|" + checkSum +"|" + data
        bytesToSend = str.encode(dataToSend)
        UDPServerSocket.sendto(bytesToSend, receiverAddress)
    elif command == "READ":
        receiver = clientMsg[1]
        msgNum = clientMsg[2]
        senderUserName = getUsername(address)
        sendAddress = getAddress(receiver)

        msgToSend = "READ" + "|" + senderUserName + "|" + msgNum
        bytesToSend = str.encode(msgToSend)
        UDPServerSocket.sendto(bytesToSend, sendAddress)
    elif command == "LEAVE":
        user = clientMsg[1]
        userAddress = getAddress(user)

        usernames.remove(user)
        addresses.remove(userAddress)

        msgToSend = "LEAVE|" + user
        bytesToSend = str.encode(msgToSend)

        for a in addresses:
            UDPServerSocket.sendto(bytesToSend, a)

