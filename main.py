# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import time
from dhooks import Webhook
from urllib.request import urlopen
from playsound import playsound
from datetime import datetime
import urllib.request
import urllib.parse
import smtplib
from email.message import EmailMessage

waitingForEmail = True
message = 'Hello,\n\nJust letting you know that the 3dscapture card is now in stock.\nGet it here quickly: https://3dscapture.com/ds/index.html\n\nGood Luck,\nChwarles.'
msg = EmailMessage()
msg.set_content(message)
msg['Subject'] = 'CAPTURE CARD IN STOCK'
msg['From'] = "emailfrom"
msg['To'] = "emailto"
password = "APASSWORD"
hook = Webhook("discordAPI webhook here")

def sendEmail():
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(msg['From'],password)
    print("Login sucess")
    server.send_message(msg)
    print("Email has been sent to ", msg['To'])
    writeInFile('Email has been sent...\n')

def checkStock():
    global waitingForEmail
    page = urlopen("https://3dscapture.com/ds/index.html")
    #page = urlopen("https://web.archive.org/web/20201221064346/https://3dscapture.com/ds/index.html")
    sitetext = page.read().decode("utf8")
    result = ''
    
    if 'SOLD OUT' in sitetext:
        result = 'out of stock'
    else:
        result = 'in stock'
        playsound('alert.wav')
        if(waitingForEmail):
            sendEmail()
            hook.send(message)
            waitingForEmail = False      
    return result

def writeInFile(text):
    f = open("logs.txt", "a")
    f.write(text)
    f.close()  

while True:
    now = datetime.now()
    current_time = now.strftime("%Y/%m/%d, %H:%M:%S")
    error = False
    try:   
        valueStock = checkStock()
    except urllib.error.URLError as e:
        print(e)
        print("error waiting 200sec...")
        writeInFile("error waiting 200sec...\n")
        time.sleep(200)
        error = True
        continue
    except urllib.error.timeout as e:
        print(e)
        print("websote timeout waiting 200sec...")
        writeInFile("websote timeout waiting 200sec...\n")
        time.sleep(200)
        error = True
        continue

    if(not error):
        print(f'{current_time} Nintendo DS USB Video Capture Board is ' + valueStock)
        writeInFile(f'{current_time} Nintendo DS USB Video Capture Board is ' + valueStock + '\n')
    else:
        writeInFile("websote timeout waiting 200sec...")

    time.sleep(30)