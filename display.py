from distutils import command
import imp
from ntpath import join
from re import X
from turtle import width
from urllib import response
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QScrollArea, QLabel, QVBoxLayout, QFormLayout, QBoxLayout, QGroupBox, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys
from http import client, server
import socket
import os
import threading
import atexit
import multiprocessing
import time

'''
Declare all GUI components
'''
app = QApplication(sys.argv)

chatWin = QMainWindow()
startUpWin = QMainWindow()
msgWin = QMainWindow()
infoWin = QMainWindow()

msgBox = QMessageBox()
msgBox.setIcon(QMessageBox.Information)

lblUserName = QtWidgets.QLabel(startUpWin)
lblIPAddress = QtWidgets.QLabel(startUpWin)
lblReceiver = QtWidgets.QLabel(chatWin)
lblInfo = QtWidgets.QLabel(infoWin)

edtUserName = QtWidgets.QLineEdit(startUpWin)
edtIPAddress = QtWidgets.QLineEdit(startUpWin)
edtMsg = QtWidgets.QLineEdit(chatWin)

btnJoinChat = QtWidgets.QPushButton(startUpWin)
btnSend = QtWidgets.QPushButton(chatWin)
btnCloseInfo = QtWidgets.QPushButton(infoWin)

lwUsers = QtWidgets.QListWidget(chatWin)
lwGroups = QtWidgets.QListWidget(chatWin)
lwMessages = QtWidgets.QListWidget(chatWin)

prog = "running"

'''
Declare all global variables and initialise with default values
'''
msgs = []
msgStatus = []
currentUsers = {}
userCount = -1

userName = ""
serverIPAddress = ""
serverAddressPort = ()
bufferSize = 1024

'''
Create UDP sockets for the client to use for communication with server.
'''
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

'''
    This method returns the width and height of the screen
    Inspired by code found at: https://www.blog.pythonlibrary.org/2015/08/18/getting-your-screen-resolution-with-python/
'''
def getScreenDimentions():
    res = app.desktop().screenGeometry()
    width, height = res.width(), res.height()
    return width, height

'''
    This method returns the number of the next message
    to be exchanged between particular users.
'''
def getNextMessageNumber(receiver):
    fileName = userName + "#" + receiver + ".txt"
    l = ""
    
    if os.path.exists(fileName):
        f = open(fileName, "r")
    
        for x in f:
            l = x
    
        f.close()

        msg = l.split("#")
        msgNum = msg[1]

        return str(int(msgNum) + 1) 
    else:
        return "1"
        
'''
    This method changes the message status from SENT to RECEIVED
    based on the parsed parameters
'''
def changeMessageStatusToReceived(msgNum, receiver):
    fileName = userName + "#" + receiver + ".txt"
    msgLines = []

    f = open(fileName, "r")
    for x in f:
        msgLines.append(x)
    f.close()

    i = 0
    msgSplit = msgLines[0].split("#")
    num = msgSplit[1]

    while num != msgNum and i < len(msgLines):
        i += 1
        msgSplit = msgLines[i].split("#")
        num = msgSplit[1]
    
    if num == msgNum:
        msgSplit[3] = "received"

    msgLines[i] = msgSplit[0] + "#" + msgSplit[1] + "#" + msgSplit[2] + "#" + msgSplit[3]    

    f = open(fileName, "w")

    for x in msgLines:
        f.write(x + "\n")
    
    f.close()

def getCheckSumValue(msg):
    vals = []

    for character in msg:
        vals.append(ord(character))
    
    sum = 0

    for v in vals:
        sum += v

    return str(sum)
'''
This method runs when the program ends.
'''
def exit_handler():
    global x, prog
    
    msgForServer = "LEAVE|" + userName
    bytesToSend = str.encode(msgForServer)

    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    prog = "not running"
    #x.terminate()
    x.join()

'''
This method sends data messages to the server and updates the relevant text file.
'''
def sendMessage():
    global userName, serverAddressPort, serverIPAddress
    receiver = lblReceiver.text()
    data = edtMsg.displayText()
    msgNum = getNextMessageNumber(receiver)
    checkSumVal = getCheckSumValue(data)

    msg = "CHAT|" + receiver + "|" + msgNum + "|" + checkSumVal + "|" + data
    bytesToSend = str.encode(msg)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    edtMsg.setText("")

    #addMessage(userName + "#" + data + "#sent")
    fileName = userName + "#" + receiver + ".txt"

    f = open(fileName, "a")
    f.write(userName + "#" + msgNum + "#" + data + "#sent\n")
    f.close()

    setUserReceiver(receiver)

'''
This method adds a message to the screen.
'''
def addMessage(msg):

    if msg != "":
        msg = msg.replace("\n", "")
        data = msg.split("#")
    
        mg = data[0] + ": " + data[2]

        if len(data) == 4:
            mg += " (" + data[3] + ")"    
    
        lwMessages.addItem(mg)

'''
This method contacts the server to try and add the user to the chat.
'''    
def joinChat():
    global userName, serverAddressPort, serverIPAddress, x
    userName = edtUserName.displayText()
    serverIPAddress = edtIPAddress.displayText()

    pkt = str.encode("JOIN|" + userName)
    
    serverAddressPort  = (serverIPAddress, 20007)

    # Send to server using this socket
    UDPClientSocket.sendto(pkt, serverAddressPort)
  
    
    # Receive response from server
    serverResponse = UDPClientSocket.recvfrom(bufferSize)
    response1 = serverResponse[0].decode()
    
    response = response1.split("|")

    if response[0] == "REJECT":
        msgBox.setText("The username you provided is already connected to the server. Please provide a different one.")
        msgBox.setWindowTitle("Server conenction error")
        msgBox.show()
        edtUserName.setText("")

    else:
        users = response[1].split("#")

        for u in users:
            if u != userName:
                addUser(u)
        
        startUpWin.hide()
        
        chatWin.setWindowTitle(userName)
        chatWin.show()
        x.start()


    #UDPClientSocket.close()

'''
This method adds the parsed username to the user list box.
'''
def addUser(user):
    global userCount

    lwUsers.addItem(user)
    userCount += 1
    currentUsers[user] = userCount

def removeUser(user):
    global userCount

    userNum = currentUsers[user]
    lwUsers.takeItem(userNum)

    userCount -= 1
    currentUsers.pop(user)

    lwMessages.clear()
    lblReceiver.setText("<none selected>")

'''
This method removes the parsed username from the user name list box.
'''
def removeUser(user):
    global userCount

    lwUsers.takeItem(currentUsers[user])
    userCount -= 1
    currentUsers.pop(user)

'''
This method is intended for adding a group name to the group list box but the group feature does not yet exist.
'''
def addGroup():
    lwi = QtWidgets.QListWidgetItem(edtMsg.displayText())

'''
    This method sets the current chat peer to whom messages can be sent and received,
    based on parsed parameter.
'''
def setUserReceiver(user=None):
    
    if user == None or not isinstance(user, str):
        lblReceiver.setText(lwUsers.currentItem().text())
    else:
        lblReceiver.setText(user)

    fileName = userName + "#" + lblReceiver.text() + ".txt"

    lwMessages.clear()
    
    rowCount = 0

    if os.path.exists(fileName):
        f = open(fileName, "r")
 
        for x in f:
            if x!= "":
                addMessage(x)
        
        f.close()

'''
This method is intended for setting the current group to which messages can be sent and received.
'''
def setGroupReceiver():
    lblReceiver.setText(lwGroups.currentItem().text())

'''
This method changes the message status.
'''
def changeMessageStatus():
    num = edtMsg.displayText()
    iNum = int(num)
    msgStatus[iNum].setText("\nreceived")

'''
This method draws the chat window.
'''    
def drawChatWindow():
    width, height = getScreenDimentions()
    row = int(height/2 - 850/2)
    col = int(width/2 - 750/2)

    chatWin.setGeometry(col, row, 850, 750)

    lblUsers = QtWidgets.QLabel(chatWin)
    lblUsers.setText("Users:")
    lblUsers.resize(500, 50)
    lblUsers.move(5, 50)
    lblUsers.setFont(QFont('Arial Rounded MT Bold', 14))

    lblGroups = QtWidgets.QLabel(chatWin)
    lblGroups.setText("Groups:")
    lblGroups.resize(500, 50)
    lblGroups.move(5, 400)
    lblGroups.setFont(QFont('Arial Rounded MT Bold', 14))

    lblReceiver.resize(500, 50)
    lblReceiver.move(220, 50)
    lblReceiver.setFont(QFont('Arial Rounded MT Bold', 14))
    lblReceiver.setText("<none selected>")

    lwUsers.resize(200, 300)
    lwUsers.move(5, 90)
    lwUsers.setFont(QFont('Arial Rounded MT Bold', 10))
    lwUsers.itemClicked.connect(setUserReceiver)

    lwGroups.resize(200, 300)
    lwGroups.move(5, 440)
    lwGroups.setFont(QFont('Arial Rounded MT Bold', 10))
    lwGroups.itemClicked.connect(setGroupReceiver)

    lwMessages.resize(600, 550)
    lwMessages.move(220, 90)
    lwMessages.setFont(QFont('Arial Rounded MT Bold', 10))

    edtMsg.resize(500, 40)
    edtMsg.move(220, 700)
    edtMsg.setFont(QFont('Arial Rounded MT Bold', 10))

    btnSend.resize(100, 40)
    btnSend.move(730, 700)
    btnSend.setText("SEND")
    btnSend.setFont(QFont('Consolas Bold', 18))
    btnSend.clicked.connect(sendMessage)

def drawStartUpWindow():
    width, height = getScreenDimentions()
    row = int(height/2 - 290/2)
    col = int(width/2 - 270/2)

    #startUpWin.setGeometry(750, 380, 290, 270)
    startUpWin.setGeometry(col, row, 290, 270)
    startUpWin.setWindowTitle("Login to Chat Application")

    lblUserName.setText("User name:")
    #lblUserName.setAlignment(QtCore.Qt.AlignRight)
    lblUserName.resize(500, 50)
    lblUserName.move(10, 10)
    lblUserName.setFont(QFont('Arial Rounded MT Bold', 14))

    edtUserName.resize(270, 40)
    edtUserName.move(10, 50)
    edtUserName.setFont(QFont('Arial Rounded MT Bold', 14))

    lblIPAddress.setText("Server IP Address:")
    lblIPAddress.resize(500, 50)
    lblIPAddress.move(10, 100)
    lblIPAddress.setFont(QFont('Arial Rounded MT Bold', 14))

    edtIPAddress.resize(270, 40)
    edtIPAddress.move(10, 140)
    edtIPAddress.setFont(QFont('Arial Rounded MT Bold', 14))

    btnJoinChat.resize(270, 60)
    btnJoinChat.move(10, 190)
    btnJoinChat.setText("Join Chat")
    btnJoinChat.setFont(QFont('Arial Rounded MT Bold', 14))
    btnJoinChat.clicked.connect(joinChat)

'''
This method runs an infinite loop on a separate thread that receives packets from the server and processes them appropriately upon arrival
'''
def receivePackets():
    global prog, serverAddressPort
    #serverAddressPort  = ("", 20007)
    bufferSize = 1024
    
    # Create a socket for UDP on the client process
    #UDPClientSocket1 = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    #UDPClientSocket1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #UDPClientSocket1.bind(serverAddressPort)
    
    while (prog == "running"):
        bytesAddressPair = UDPClientSocket.recvfrom(bufferSize)


        message = bytesAddressPair[0]
        message = message.decode()
        message = message.split("|")
        command = message[0]

        if command == "ADD":
            if message[1] != userName:
                addUser(message[1])
        elif command == "SUB":
            removeUser(message[1])
        elif command == "CHAT":
            sender = message[1]
            msgNum = message[2]
            checkSumVal = message[3]
            data = message[4]
            
            fileName = userName + "#" + sender + ".txt"

            f = open(fileName, "a")
            f.write(sender + "#" + msgNum + "#" + data + "\n")
            f.close()

            returnMsg = "READ|" + sender + "|" + msgNum
            bytesToSend = str.encode(returnMsg)
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)

            setUserReceiver(sender)
            '''
            msgBox.setWindowTitle("Message Received")
            msgBox.setText("A message has been received from " + sender)
            msgBox.setDetailedText(data)
            msgBox.show()
            '''
        elif command == "READ":
            sender = message[1]
            msgNum = message[2]

            changeMessageStatusToReceived(msgNum, sender)
            setUserReceiver(sender)
        elif command == "LEAVE":
            userToRemove = message[1]
            removeUser(userToRemove)

'''
This method is called once all global variables have been declared and all necessary functions have been defined. 
'''
def main():
    global x
    drawStartUpWindow()
    drawChatWindow()
    startUpWin.show()
    x = threading.Thread(target=receivePackets)
    x.daemon = True
    atexit.register(exit_handler)
    sys.exit(app.exec_())


main()