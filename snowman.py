import RPi.GPIO as GPIO
import time
import random
import sys
from datetime import datetime

pinButton = 21
pinRed = 19
pinGreen = 17
pinBlue = 13

color_palette = [
	(0,0,255),
	(179,12,0),
	(220,42,61),
	(13,66,239),
	(0,44,179),
	(13,1,89),
	(255,0,0),
	(255,120,120),
	(255,255,255),
	(116,129,214),
	(55,41,139)
]


def setup():
	global pwmRed, pwmBlue, pwmGreen
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(pinRed, GPIO.OUT)
	GPIO.setup(pinGreen, GPIO.OUT)
	GPIO.setup(pinBlue, GPIO.OUT)
	GPIO.setup(pinButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	GPIO.output(pinRed, GPIO.HIGH)
	GPIO.output(pinGreen, GPIO.HIGH)
	GPIO.output(pinBlue, GPIO.HIGH)
	pwmRed = GPIO.PWM(pinRed, 2000)
	pwmGreen = GPIO.PWM(pinGreen, 2000)
	pwmBlue = GPIO.PWM(pinBlue, 2000)

	pwmRed.start(0)
	pwmGreen.start(0)
	pwmBlue.start(0)


def setColour(red: int, green: int, blue: int):
	r = (red/255)*100
	g = (green/255)*100
	b = (blue/255)*100
	pwmRed.ChangeDutyCycle(r)
	pwmGreen.ChangeDutyCycle(g)
	pwmBlue.ChangeDutyCycle(b)
	#print('r,b,g = %d,%d,%d') % (r,b,g)


def loop(timer: int = 3):
	print('Starting up')
	current_colour = None
	running = True
	starttime = int(datetime.now().timestamp())-timer
	buttontime = int(datetime.now().timestamp())
	buttontimeout = 2
	while True:
		if GPIO.input(pinButton) == GPIO.LOW:
			if int(datetime.now().timestamp()) >= buttontime+buttontimeout:
				running = not running
				buttontime = int(datetime.now().timestamp())
				print('Swapping state : %s' % running)
		
		if running:
			tnow = int(datetime.now().timestamp())
			if int(tnow) >= starttime+timer:
				new_colour = random.randint(0,len(color_palette)-1)
				if current_colour is None or current_colour != new_colour:
					setColour(color_palette[new_colour][0], 
						color_palette[new_colour][1], 
						color_palette[new_colour][2])
					current_colour = new_colour
					starttime = int(datetime.now().timestamp())
		else:
			setColour(0,0,0)
			


def destroy():
	print('Stopping')
	pwmRed.stop()
	pwmBlue.stop()
	pwmGreen.stop()
	GPIO.cleanup()


if __name__ == '__main__':
	timer = 3
	setup()
	try:
		loop(timer=timer)
	except KeyboardInterrupt:
		destroy()

