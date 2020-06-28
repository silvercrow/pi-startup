# Importing socket library 

import socket
import evdev
import picamera
from subprocess import check_output
from evdev import InputDevice, categorize, ecodes
import sys
import os
import random
import datetime
import time
wallpaperDir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'wallpapers')
cameraDir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'camera')
fontsDir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'fonts')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback


devices =[InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    if str(device.name) == 'Selfie Stick AU-Z06 Consumer Control':
        selfieStick = device

selfieStickBtn = 115


def printToPaper(text):
    logging.info("print to paper")
    epd = epd2in13_V2.EPD()
    logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    # Drawing on the image
    smallText = ImageFont.truetype(os.path.join(fontsDir, 'Poppins-SemiBold.ttf'), 18)
    #logging.info("1.Drawing on the image...")
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
    draw = ImageDraw.Draw(image)
    draw.text((20, 5), text, font = smallText, fill = 0)
    epd.display(epd.getbuffer(image))
    time.sleep(2)
    
def printPicture(img):
    logging.info("Wallpaper")
    epd = epd2in13_V2.EPD()
    logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    logging.info("reading image file...")
    image = Image.open(os.path.join(cameraDir, img))
    epd.display(epd.getbuffer(image))
    time.sleep(2)
    logging.info("Goto Sleep...")



def takeMyPicture():
    date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
    img = date+'.jpg'
    logging.info("taking a picture :",img)
    camera = picamera.PiCamera()
    camera.resolution =(122,250)
    camera.color_effects =(128,128)
    camera.capture('camera/'+img)
    camera.close()
    printPicture(img)
    
# Function to display hostname and 
# IP address 
def get_Host_name_IP(): 
    try: 
        ip =str(check_output(['hostname', '-I']).strip()).replace("b'","").replace("'","")
        print("IP :  ",ip) 
        hostnameIP = str("IP : "+ip+" ")
        printToPaper(hostnameIP)
        
    except: 
        print("Unable to get Hostname and IP") 

def printWallpaper():
    logging.info("Wallpaper")
    epd = epd2in13_V2.EPD()
    logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    wallpaper = 'wallpaper-'+str(random.randint(1,4))+'.jpg'
    logging.info("reading image file...")
    image = Image.open(os.path.join(wallpaperDir, wallpaper))
    epd.display(epd.getbuffer(image))
    time.sleep(2)
    logging.info("Goto Sleep...")

logging.basicConfig(level=logging.DEBUG)
get_Host_name_IP()



try:
    logging.info("Wallpaper-Pi")
    #loop and filter by event code and print the mapped label
    for event in selfieStick.read_loop():
        if event.type == ecodes.EV_KEY:
            if event.value == 1:
                if event.code == selfieStickBtn:
                   takeMyPicture()
                   #printWallpaper()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()



