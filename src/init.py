# Importing socket library 
import socket 
from evdev import InputDevice, categorize, ecodes
import sys
import os
import random
wallpaperDir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'wallpapers')
fontsDir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'fonts')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback



#creates object 'gamepad' to store the data
#you can call it whatever you like
gamepad = InputDevice('/dev/input/event1')

#prints out device info at start
print(gamepad)
selfieStickBtn = 115


def printToPaper(text):
    # Drawing on the image
    epd = epd2in13_V2.EPD()
    smallText = ImageFont.truetype(os.path.join(fontsDir, 'Poppins-SemiBold.ttf'), 18)
    #logging.info("1.Drawing on the image...")
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), text, font = smallText, fill = 0)
    epd.display(epd.getbuffer(image))
    time.sleep(2)

# Function to display hostname and 
# IP address 
def get_Host_name_IP(): 
    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        socketName =s.getsockname()[0]
        printToPaper(str(socketName))
        s.close()
        
    except: 
        print("Unable to get Hostname and IP") 

def printWallpaper():
    wallpaper = 'wallpaper-'+str(random.randint(1,4))+'.jpg'
    epd = epd2in13_V2.EPD()
    logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
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
    for event in gamepad.read_loop():
        if event.type == ecodes.EV_KEY:
            if event.value == 1:
                if event.code == selfieStickBtn:
                    printWallpaper()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()



