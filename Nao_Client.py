# coding=utf-8
import os
import sys
import time
import paramiko
import logging
from naoqi import ALProxy

# Replace this with your robot's IP address

IP = "192.168.1.131"
PORT = 9559

# Create a proxy to ALPhotoCapture
photoCaptureProxy = ALProxy("ALPhotoCapture", IP, PORT)
# Take 3 pictures in VGA and store them in /home/nao/recordings/cameras/
tts = ALProxy("ALTextToSpeech", IP, PORT)
tts.say("Hello!")
tts.say("I will recognize your emotion !")
tts.say("Just a moment I'll look at you and tell you !")

# tts=ALProxy("ALTextToSpeech", IP, PORT)
tts.say("Say Cheeeeeese !")

print("NAO is taking the picture, try not to move!")

photoCaptureProxy.setResolution(2)
photoCaptureProxy.setPictureFormat("jpg")
photoCaptureProxy.takePictures(3, '/home/nao/recordings/cameras/', "image")

tts.say("Picture taken !")

print("NAO took the picture!")

# This call returns ['/home/nao/recordings/cameras/image_0.jpg', '/home/nao/recordings/cameras/image_1.jpg', '/home/nao/recordings/cameras/image_2.jpg']


# Download dalla memoria interna di NAO, della foto appena scattata

NAO_USERNAME = "nao"
NAO_PASSWORD = "nao6"

# Importo i log
logging.basicConfig()
log = logging.getLogger("provoTrasferimentoDati")
log.setLevel(logging.DEBUG)
log.info("Prova del log")

log.info("Testo il trasferimento del file")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
log.info("Provo la connessione")

ssh.connect(IP, username=NAO_USERNAME, password=NAO_PASSWORD)
log.info("Connessione stabilita")
log.info("Provo a ad aprire la connessine sftp")
sftp = ssh.open_sftp()
log.info("Connessione aperta")
localpath = r"C:\Users\CasaLab1\PycharmProjects\NAOTesiProject\foto.png"  # Attention at the path
remotepath = '/home/nao/recordings/cameras/image_1.jpg'
log.info("faccio il get")
sftp.get(remotepath, localpath)
log.info("File trasferito")
log.info("Chiudo le connessioni")
#sftp.close()
#ssh.close()
log.info("Connessione chiusa")
log.info("Programma terminato")

##########################

import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
client.connect(('127.0.0.1', 10000))  #localhost='127.0.0.1'

file = open('foto.png', 'rb')  #Foto scattata da NAO
image_nao = file.read(2048)

while image_nao:
    client.send(image_nao)
    image_nao = file.read(2048)

file.close()
client.close()

##########################

tts.say("One moment, please !")
time.sleep(6)

#!/usr/bin/python
# -*- coding: ascii -*-

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
client.connect(('127.0.0.1', 22222))  # localhost='127.0.0.1'

msg = client.recv(1024)   # Ricevera' la stringa del messaggio di risposta dal server a 1024 bit

while msg:
  print('Result of recognition: ' + msg.decode())
  esito = msg.decode()
  msg = client.recv(1024)   # Verra' eseguito finche' la stringa del messaggio e' vuota

  tts.say('Your recognized emotion is:: ' + str(esito)) #NAO states the result of the recognition

client.close()  # Disconnettera' il client

sftp.close()
ssh.close()