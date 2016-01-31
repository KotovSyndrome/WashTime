import RPi.GPIO as GPIO
import smbus
import math
import numpy as np
import time
import urllib
import urllib2

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
OPEN=False
IN_USE=True
# implement gyro
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
testBinary=22
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

bus = smbus.SMBus(1)
address=0x68
bus.write_byte_data(address, power_mgmt_1, 0)


def machine_vibrate(adr):
	machine_vibrate = False
	accel_xout = read_word_2c(adr)
	xTempValues=range(5)
	realTime=0
	xAxis=0
	while(realTime<4):
		xTempValues[realTime]=accel_xout
		time.sleep(0.5)
		realTime+=1

	jerk=np.std(xTempValues, axis=0)
	if(jerk>300):
		machine_vibrateX= True
	else: 
		machine_vibrateX= False

	return machine_vibrateX

def reed_switch_status(pin):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(17, GPIO.IN)
	if GPIO.input(17):
		return False
	else:
		return True
	GPIO.cleanup()

def cycle_parse(reed_switch_status, machine_vibrate):
	testBinary=0
	if(machine_vibrate==True):
		if(reed_switch_status==True):
			testBinary="11"
			return testBinary
		elif(reed_switch_status==False):
			testBinary="01"
			return testBinary
	elif(machine_vibrate==False):
		testBinary="00"
		return testBinary

def post_sleep_cycle(reed_status):
	print"waiting 20"
	while(reed_status==True):
		time.sleep(20)
		print("reading reed_switch_status")
		if(reed_switch_status(17)==False):
			break



def push_data(machine_status):
	query_args={'machine_status':machine_status}
	data = urllib.urlencode(query_args)
	print 'Encoded: ', data
	url = "http://54.200.245.42/firebaseTest.php?"+data
	print urllib.urlopen(url).read()
	if(machine_status=="11"):
		reed_switch_status=True
		print "waiting 10"
		time.sleep(10)
		print"running post_sleep_cycle"
		post_sleep_cycle(reed_switch_status)

while True:
	push_data(cycle_parse(reed_switch_status(17), machine_vibrate(0x43)))
	print "%s and %s" %(reed_switch_status(17), machine_vibrate(0x43))
	#door_closed=1 vibrating=1