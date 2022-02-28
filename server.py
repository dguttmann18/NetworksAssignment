from ipaddress import ip_address
import socket
import sys

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024
hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)

msgFromServer       = "Hello UDP Client"
bytesToSend         = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((IP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams
while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]

    clientMsg = message.decode()
    clientIP  = "Client IP Address:{}".format(address)
    
    comp = clientMsg.split("#")
    nme = comp[0]
    msg = comp[1]

    print(nme + ": " + msg)
    print(clientIP)

    # Sending a reply to client
    #UDPServerSocket.sendto(bytesToSend, address)

    if clientMsg == "quit":
        sys.exit()

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