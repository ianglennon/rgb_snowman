from rpi-RGBSnowman import RGBSnowman, State
import RPi.GPIO as GPIO
import signal
from datetime import datetime


def loop(snowman: RGBSnowman):
	start_time = int(datetime.now().timestamp()) - snowman.pause_time
	button_time = int(datetime.now().timestamp())
	button_timeout = 2
	while True:
		if GPIO.input(snowman.pin_button) == GPIO.LOW:
			if int(datetime.now().timestamp()) >= button_time + button_timeout:
				snowman.button_press()
				button_time = int(datetime.now().timestamp())

		if snowman.state != State.STOPPED:
			t_now = int(datetime.now().timestamp())
			if int(t_now) >= start_time + snowman.pause_time:
				snowman.change_colour(with_set=True)
				start_time = int(datetime.now().timestamp())


if __name__ == '__main__':
	sman = RGBSnowman(pin_button=21, pin_red=19, pin_green=17, pin_blue=13, fade_time=1, pause_time=1)
	sman.start()

	def signal_shutdown(signum, frame):
		sman.shutdown()

	def signal_status_change(signum, frame):
		sman.button_press()

	def signal_colour_change(signum, frame):
		sman.change_colour(with_set=True)

	signal.signal(signal.SIGHUP, signal_colour_change)
	signal.signal(signal.SIGBREAK, signal_shutdown)
	signal.signal(signal.SIGKILL, signal_shutdown)
	signal.signal(signal.SIGSTOP, signal_shutdown)
	signal.signal(signal.SIGUSR1, signal_status_change)

	try:
		loop(snowman=sman)
	except KeyboardInterrupt:
		sman.shutdown()
