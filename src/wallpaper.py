from evdev import InputDevice, categorize, ecodes
import sys
import os
import random
wallpaperDir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'wallpapers')
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




