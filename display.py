import imp
from ntpath import join
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QScrollArea, QLabel, QVBoxLayout, QFormLayout, QBoxLayout, QGroupBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys

app = QApplication(sys.argv)

chatWin = QMainWindow()
startUpWin = QMainWindow()

lblUserName = QtWidgets.QLabel(startUpWin)
lblIPAddress = QtWidgets.QLabel(startUpWin)

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

def joinChat():
     startUpWin.hide()
     chatWin.show()

def addUser():
    lwi = QtWidgets.QListWidgetItem(edtMsg.displayText())
    lwUsers.addItem(lwi)

def removeUser():
    lwUsers.takeItem(lwUsers.currentRow())

def addGroup():
    lwi = QtWidgets.QListWidgetItem(edtMsg.displayText())

def showItem():
    print(lwUsers.currentItem().text())

def addButton():
    btn = QtWidgets.QPushButton(chatWin)
    btn.resize(100, 40)
    btn.setText("Hello World")
    msgArea.addScrollBarWidget(btn, Qt.AlignLeft)
    
def drawChatWindow():
    chatWin.setGeometry(600, 100, 850, 750)
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

    lwUsers.resize(200, 300)
    lwUsers.move(5, 90)
    lwUsers.setFont(QFont('Arial Rounded MT Bold', 10))
    lwUsers.itemClicked.connect(showItem)
    QtWidgets.QListWidgetItem("Danny", lwUsers)
    QtWidgets.QListWidgetItem("Michael", lwUsers)
    QtWidgets.QListWidgetItem("Sizwe", lwUsers)

    lwGroups.resize(200, 300)
    lwGroups.move(5, 440)
    lwGroups.setFont(QFont('Arial Rounded MT Bold', 10))
    #lwGroups.itemClicked.connect(showItem(lwGroups))
    QtWidgets.QListWidgetItem("Computer Science", lwGroups)
    QtWidgets.QListWidgetItem("Mathematic", lwGroups)
    QtWidgets.QListWidgetItem("Economics", lwGroups)

    edtMsg.resize(500, 40)
    edtMsg.move(220, 700)
    edtMsg.setFont(QFont('Arial Rounded MT Bold', 10))

    btnSend.resize(100, 40)
    btnSend.move(730, 700)
    btnSend.setText("SEND")
    btnSend.setFont(QFont('Consolas Bold', 18))
    btnSend.clicked.connect(addButton)

    '''
    msgArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
    msgArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    msgArea.setWidgetResizable(True)
    msgArea.resize(650, 850)
    msgArea.move(220, 90)
    '''

    for i in range(100):
        msgs.append(QLabel("Hello World!"))
        formLayout.addRow(msgs[i])

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
    startUpWin.setGeometry(750, 380, 290, 270)
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


def main():
    drawStartUpWindow()
    drawChatWindow()
    startUpWin.show()
    sys.exit(app.exec_())

main()