import os
import glob
import time
import sys
import datetime
import urllib2
import RPi_I2C_driver
from time import *

baseURL = "https://api.thingspeak.com/update?api_key=BCQOBOXNDHS4L81T"
 
os.system('modprobe w1-gpio')
 
os.system('modprobe w1-therm')
 
base_dir = 'sys/bus/w1/devices/'
 
#water temperature device location
watertemp_file = '/sys/bus/w1/devices/28-0414694e4eff/w1_slave'
 
mylcd = RPi_I2C_driver.lcd()

#Determine water temperature
def read_rawwatertemp():
     f = open(watertemp_file,'r')
     lines = f.readlines()
     f.close
     return lines
 
def read_watertemp():
     lines = read_rawwatertemp()
     while lines[0].strip()[-3:] !='YES':
          time.sleep(0.2)
          lines = read_rawwatertemp()
     equals_pos = lines[1].find('t=')
     if equals_pos !=-1:
          temp_string = lines[1][equals_pos+2:]
          temp_water = float(temp_string)/1000.0
          return temp_water

block = chr(255) # block character, built-in
custom_pause = 0.2 # define duration of sleep(x)

# now draw cust. chars starting from col. 7 (pos. 6)

pos = 6
mylcd.lcd_display_string_pos(unichr(1),2,6)
sleep(custom_pause)

mylcd.lcd_display_string_pos(unichr(2),2,pos)
sleep(custom_pause)

mylcd.lcd_display_string_pos(unichr(3),2,pos)
sleep(custom_pause)

mylcd.lcd_display_string_pos(unichr(4),2,pos)
sleep(custom_pause)

mylcd.lcd_display_string_pos(block,2,pos)
sleep(custom_pause)

# and another one, same as above, 1 char-space to the right
pos = pos +1 # increase column by one

mylcd.lcd_display_string_pos(unichr(1),2,pos)
sleep(custom_pause)
mylcd.lcd_display_string_pos(unichr(2),2,pos)
sleep(custom_pause)
mylcd.lcd_display_string_pos(unichr(3),2,pos)
sleep(custom_pause)
mylcd.lcd_display_string_pos(unichr(4),2,pos)
sleep(custom_pause)
mylcd.lcd_display_string_pos(block,2,pos)
sleep(custom_pause)

while True: #Loop

#Send water Temperature to Thingspeak
     water_temp = read_watertemp()
     water_temp = (water_temp * 1.8) + 32

#Pull results together
     values = [datetime.datetime.now(), water_temp]
 
#Open Thingspeak channel and assign fields to temperatures
     j = urllib2.urlopen(baseURL + "&field1=%s" % (water_temp))

     mylcd.lcd_display_string("Temp:" + str(water_temp), 1)

#Time to next loop
time.sleep(3000)