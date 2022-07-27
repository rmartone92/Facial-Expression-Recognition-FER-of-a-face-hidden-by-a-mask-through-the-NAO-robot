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

# Take one pictures in VGA and store them in /home/nao/recordings/cameras/

tts = ALProxy("ALTextToSpeech", IP, PORT)

# NAO speaks

tts.say("Hello !")

tts.say("I will recognize your emotion !")

tts.say("Just a moment I'll look at you and tell you !")

tts.say("Say Cheeeeeese !")

print("NAO is taking the picture, try not to move!")

photoCaptureProxy.setResolution(2)
photoCaptureProxy.setPictureFormat("png")
photoCaptureProxy.takePictures(1, '/home/nao/recordings/cameras/', "image")

tts.say("Picture taken !")

print("NAO took the picture!")

# This call returns ['/home/nao/recordings/cameras/image_0.jpg']

# Download from the internal memory of NAO, of the photo just taken

# Credentials to enter NAO's memory:

NAO_USERNAME = "nao"
NAO_PASSWORD = "nao6"

# Log

logging.basicConfig()
log = logging.getLogger("I try data transfer")
log.setLevel(logging.DEBUG)
log.info("Test the logs")

log.info("I try the file transfer")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
log.info("I try the connection")

ssh.connect(IP, username=NAO_USERNAME, password=NAO_PASSWORD)
log.info("Connection established")
log.info("I try to open the sftp connection")
sftp = ssh.open_sftp()
log.info("Open connection")
localpath = r"C:\Users\CasaLab1\PycharmProjects\NAOTesiProject\photo_taken.png"  # Attention at the path

#Photo taken by NAO
#This photo will remain local and will be overwritten every time

remotepath = '/home/nao/recordings/cameras/image_0.jpg'
log.info("I do the get")
sftp.get(remotepath, localpath)
log.info("File transferred")
log.info("I close the connections later")

#sftp.close()
#ssh.close()
# They were closed after

# Sending photos to the server

import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
client.connect(('127.0.0.1', 10000))  #localhost='127.0.0.1'

file = open('photo_taken.png', 'rb')

image_nao = file.read(2048)

while image_nao:
    client.send(image_nao)
    image_nao = file.read(2048)

file.close()
client.close()

# Photo sent, Nao asks to wait a moment

tts.say("One moment, please !")

time.sleep(6)

#!/usr/bin/python
# -*- coding: ascii -*-

# The client receives the recognize result

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
client.connect(('127.0.0.1', 22222))  # localhost='127.0.0.1'

msg = client.recv(1024)   # It will receive the response message string from the server at 1024 bits

while msg:
  print('Result of recognition: ' + msg.decode())
  esito = msg.decode()
  msg = client.recv(1024)   # It will be executed as long as the message string is empty

  tts.say('Your recognized emotion is:: ' + str(esito)) #NAO states the result of the recognition

client.close()  # The client will disconnect

# Close connections

sftp.close()
ssh.close()