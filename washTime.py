# initialize GPIO, look at reedread.py
import RPi.GPIO as GPIO
import smbus
import math
import numpy as np
import time
import urllib
import urllib2

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

DOOR_OPEN = None

if GPIO.input(17):
	 DOOR_OPEN = True;
else:
	DOOR_OPEN = False;
GPIO.cleanup()

# implement gyro
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
def read_byte(adr):
	return bus.read_byte_data(address, adr)

def read_word(adr):
	high = bus.read_byte_data(address, adr)
	low = bus.read_byte_data(address, adr+1)
	val = (high << 8) + low
	return val

def read_word_2c(adr):
	val=read_word(adr)
	if(val>0x8000):
		return-((65535-val)+1)
	else:
		return val

def dist(a,b):
	return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
	radians=math.atan2(x, dist(y,z))
	return -math.degrees(radians)

def get_x_rotation(x,y,z):
	radians=math.atan2(y, dist(x,z))
	return math.degrees(radians)

bus = smbus.SMBus(1)
address=0x68
bus.write_byte_data(address, power_mgmt_1, 0)
print "gyro data"
print "-------------"

accel_xout = read_word_2c(0x43)
accel_yout = read_word_2c(0x45)
accel_zout = read_word_2c(0x47)

accel_xout_scaled = accel_xout / 16384.0
accel_yout_scaled = accel_yout / 16384.0
accel_zout_scaled = accel_zout / 16384.0

#print "accel_xout", accel_xout, " scaled: ", accel_xout_scaled
#print "accel_yout", accel_yout, " scaled: ", accel_yout_scaled
#print "accel_zout", accel_zout, " scaled: ", accel_zout_scaled

#print "x rotation: ", get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
#print "y rotation: ", get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

# the meat of the code is here
accel_xout=read_word_2c(0x43)
xTempValues=range(5)
realTime=0
axis=0
while(realTime<4):
	xTempValues[realTime]=accel_xout
	time.sleep(1)
	realTime+=1

jerk=np.std(xTempValues, axis=0)
if(jerk>300):
	machine_status='True'
else: 
	machine_status='False'

query_args={'machine_status':machine_status}

data = urllib.urlencode(query_args)

print 'Encoded: ', data

url = "http://54.200.245.42/firebaseTest.php?"+data

print urllib.urlopen(url).read()

#def reed_switch_status():
	# if reed switch is on, return DOOR_CLOSED
	
#def cycle_parse():
	# if is_gyro_moving is true, delay 1.8x10^6 seconds, set machine_state to BUSY, and after delay while(reed_switch_status), return BUSY
	# return OPEN, loop OPEN while(!is_gyro_moving)
	
#def push_data():
	# POST cycle_parse