from http import client, server
import socket

msgFromClient       = input("Please type your message here:")
bytesToSend         = str.encode(msgFromClient)
hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)
serverAddressPort   = (IP, 20001)
bufferSize          = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

#msgFromServer = UDPClientSocket.recvfrom(bufferSize)

'''
sName = "local host"
sPort = 20000
cSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
message = input("Enter a sentence: ")
cSocket.sendto(message.encode(), (sName, sPort))
modifiedMessage, sAddress = cSocket.recvfrom(2048)
print(modifiedMessage.decode())
cSocket.close()
'''