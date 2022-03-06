from distutils import command
import imp
from ntpath import join
from turtle import width
from urllib import response
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QScrollArea, QLabel, QVBoxLayout, QFormLayout, QBoxLayout, QGroupBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys
from http import client, server
import socket
import os.path
import threading

app = QApplication(sys.argv)

chatWin = QMainWindow()
startUpWin = QMainWindow()
msgWin = QMainWindow()

lblUserName = QtWidgets.QLabel(startUpWin)
lblIPAddress = QtWidgets.QLabel(startUpWin)
lblReceiver = QtWidgets.QLabel(chatWin)

edtUserName = QtWidgets.QLineEdit(startUpWin)
edtIPAddress = QtWidgets.QLineEdit(startUpWin)
edtMsg = QtWidgets.QLineEdit(chatWin)

btnJoinChat = QtWidgets.QPushButton(startUpWin)
btnSend = QtWidgets.QPushButton(chatWin)

lwUsers = QtWidgets.QListWidget(chatWin)
lwGroups = QtWidgets.QListWidget(chatWin)

msgArea = QScrollArea()

formLayout = QFormLayout()
groupBox = QGroupBox("")

msgs = []
msgStatus = []
currentUsers = {}
userCount = -1

userName = ""
serverIPAddress = ""
serverAddressPort = ()
bufferSize = 1024
'''
    This method returns the width and height of the screen
    Inspired by code found at: https://www.blog.pythonlibrary.org/2015/08/18/getting-your-screen-resolution-with-python/
'''
def getScreenDimentions():
    res = app.desktop().screenGeometry()
    width, height = res.width(), res.height()
    return width, height

def join():
    startUpWin.hide()
    chatWin.show()

def joinChat():
    userName = edtUserName.displayText()
    serverIPAddress = edtIPAddress.displayText()

    pkt = str.encode("JOIN|" + userName)
    print(userName)
    
    serverAddressPort  = (serverIPAddress, 20007)
    
    # Create a socket for UDP on the client process
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Send to server using this socket
    UDPClientSocket.sendto(pkt, serverAddressPort)
    
    # Receive response from server
    serverResponse = UDPClientSocket.recvfrom(bufferSize)
    response1 = serverResponse[0].decode()
    print(response1)
    
    response = response1.split("|")
    print(str(response))

    if response[0] == "REJECT":
        print("The username you provided is already connected to the server. Please provide a different one.")
        edtUserName.setText("")

    else:
        users = response[1].split("#")
        print(str(users))

        for u in users:
            if u != userName:
                addUser(u)
        
        startUpWin.hide()
        chatWin.show()
        x = threading.Thread(target=receivePackets)
        x.start()


    UDPClientSocket.close()

def addUser(user):
    global userCount

    lwUsers.addItem(user)
    userCount += 1
    currentUsers[user] = userCount

def removeUser(user):
    global userCount

    lwUsers.takeItem(currentUsers[user])
    userCount -= 1
    currentUsers.pop(user)

def addGroup():
    lwi = QtWidgets.QListWidgetItem(edtMsg.displayText())

def setUserReceiver():
    lblReceiver.setText(lwUsers.currentItem().text())

def setGroupReceiver():
    lblReceiver.setText(lwGroups.currentItem().text())

def addButton():
    btn = QtWidgets.QPushButton(chatWin)
    btn.resize(100, 40)
    btn.setText("Hello World")
    msgArea.addScrollBarWidget(btn, Qt.AlignLeft)

def changeMessageStatus():
    num = edtMsg.displayText()
    print(num)
    iNum = int(num)
    msgStatus[iNum].setText("\nreceived")
    
def drawChatWindow():
    width, height = getScreenDimentions()
    row = int(height/2 - 850/2)
    col = int(width/2 - 750/2)

    chatWin.setGeometry(col, row, 850, 750)
    chatWin.setWindowTitle("Display Window")

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

    edtMsg.resize(500, 40)
    edtMsg.move(220, 700)
    edtMsg.setFont(QFont('Arial Rounded MT Bold', 10))

    btnSend.resize(100, 40)
    btnSend.move(730, 700)
    btnSend.setText("SEND")
    btnSend.setFont(QFont('Consolas Bold', 18))
    btnSend.clicked.connect(changeMessageStatus)

    '''
    msgArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
    msgArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    msgArea.setWidgetResizable(True)
    msgArea.resize(650, 850)
    msgArea.move(220, 90)
    '''

    for i in range(100):
        body = QLabel()

        if i % 2 == 0: 
            body.setText("Hello World! Message number " +  str(i))
        else:
            body.setText("    Hello World! Message number " +  str(i))
        
        body.setFont(QFont('Arial Rounded MT Bold', 12))

        det = QLabel()
        det.setText("\nsent")
        det.setAlignment(QtCore.Qt.AlignRight)
        det.setFont(QFont('Arial Rounded MT Bold', 8))
        
        msgs.append(body)
        msgStatus.append(det)
        formLayout.addRow(msgs[i], msgStatus[i])
        formLayout.setVerticalSpacing(20)

    groupBox.setLayout(formLayout)
    scroll = QScrollArea(chatWin)
    scroll.setWidget(groupBox)
    scroll.setWidgetResizable(True)
    scroll.setFixedHeight(600)
    scroll.setFixedWidth(608)
    scroll.move(220, 90)

    layout = QVBoxLayout()
    layout.addWidget(scroll)


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

def receivePackets():
    print("Inside thread")
    serverAddressPort  = (serverIPAddress, 20007)
    bufferSize = 1024
    
    # Create a socket for UDP on the client process
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    UDPClientSocket.bind(serverAddressPort)
    
    while (True):
        bytesAddressPair = UDPClientSocket.recvfrom(bufferSize)

        message = bytesAddressPair[0]
        message = message.decode()
        print(message)
        message = message.split("|")
        command = message[0]

        if command == "ADD":
            if message[1] != userName:
                addUser(message[1])
        elif command == "SUB":
            removeUser(message[1])
        #elif command == "CHAT":


def main():
    drawStartUpWindow()
    drawChatWindow()
    startUpWin.show()
    sys.exit(app.exec_())

main()