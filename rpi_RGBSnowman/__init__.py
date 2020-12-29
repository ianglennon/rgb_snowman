import RPi.GPIO as GPIO
import time
import random
from enum import Enum


class State(Enum):
    STOPPED = 1
    SWAP_STANDARD = 2
    FADE_STANDARD = 3
    FTB_STANDARD = 4


class RGBSnowman:
    pin_button: int
    pin_red: int
    pin_green: int
    pin_blue: int
    fade_time: int
    pause_time: int
    pwm_red: GPIO.PWM
    pwm_green: GPIO.PWM
    pwm_blue: GPIO.PWM
    state: State
    current_colour: tuple

    standard_palette = [
        (0, 0, 255),
        (179, 12, 0),
        (220, 42, 61),
        (13, 66, 239),
        (0, 44, 179),
        (13, 1, 89),
        (255, 0, 0),
        (255, 120, 120),
        (255, 255, 255),
        (116, 129, 214),
        (55, 41, 139)
    ]

    def __init__(self, pin_button: int = None, pin_red: int = None, pin_green: int = None, pin_blue: int = None,
                 fade_time: int = 1, pause_time: int = 1):
        if pin_red:
            self.pin_red = pin_red
        if pin_button:
            self.pin_button = pin_button
        if pin_green:
            self.pin_green = pin_green
        if pin_blue:
            self.pin_blue = pin_blue

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.pin_red, GPIO.OUT)
        GPIO.setup(self.pin_green, GPIO.OUT)
        GPIO.setup(self.pin_blue, GPIO.OUT)
        GPIO.setup(self.pin_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.output(self.pin_red, GPIO.HIGH)
        GPIO.output(self.pin_green, GPIO.HIGH)
        GPIO.output(self.pin_blue, GPIO.HIGH)
        self.pwm_red = GPIO.PWM(self.pin_red, 2000)
        self.pwm_green = GPIO.PWM(self.pin_green, 2000)
        self.pwm_blue = GPIO.PWM(self.pin_blue, 2000)
        self.state = State.STOPPED
        self.current_colour = (0, 0, 0)
        self.fade_time = fade_time
        self.pause_time = pause_time

    def change_colour(self, palette: list = None, with_set=False):
        if palette is None:
            palette = self.standard_palette
        new_colour_idx = random.randint(0, len(palette) - 1)
        new_colour = palette[new_colour_idx]
        if self.current_colour is None:
            self.current_colour = (0, 0, 0)
        if self.current_colour != new_colour:
            if with_set:
                if self.state == State.SWAP_STANDARD:
                    self.set_colour(new_colour)
                elif self.state == State.FADE_STANDARD:
                    self.fade_colour(new_colour=new_colour)
                elif self.state == State.FTB_STANDARD:
                    self.ftb_colour(new_colour=new_colour)
            self.current_colour = new_colour
            return
        else:
            self.change_colour(palette=palette, with_set=with_set)

    def fade_colour(self, new_colour: tuple):
        old_colour = self.current_colour
        fade_time = self.fade_time
        slice_time = fade_time / 1000
        r_diff = (new_colour[0] - old_colour[0]) / 1000
        g_diff = (new_colour[1] - old_colour[1]) / 1000
        b_diff = (new_colour[2] - old_colour[2]) / 1000
        for i in range(0, 1000, 1):
            if self.state.value == 0:
                self.set_colour((0, 0, 0))
                self.stop()
                return (0, 0, 0)
            i_colour = (old_colour[0] + (r_diff * i), old_colour[1] + (g_diff * i), old_colour[2] + (b_diff * i))
            self.set_colour(i_colour)
            time.sleep(slice_time)
        self.set_colour(new_colour)
        return new_colour

    def ftb_colour(self, new_colour: tuple):
        old_colour = self.current_colour
        fade_time = self.fade_time
        slice_time = fade_time / 1000
        r_diff = old_colour[0] / 1000
        g_diff = old_colour[1] / 1000
        b_diff = old_colour[2] / 1000
        for i in range(0, 1000, 1):
            if self.state.value == 0:
                self.set_colour((0, 0, 0))
                self.stop()
                return (0, 0, 0)
            i_colour = (old_colour[0] + (r_diff * i), old_colour[1] + (g_diff * i), old_colour[2] + (b_diff * i))
            self.set_colour(i_colour)
            time.sleep(slice_time)
        self.set_colour((0, 0, 0))
        time.sleep(self.pause_time)
        r_diff = new_colour[0] / 1000
        g_diff = new_colour[1] / 1000
        b_diff = new_colour[2] / 1000
        for i in range(0, 1000, 1):
            if self.state.value == 0:
                self.set_colour((0, 0, 0))
                self.stop()
                return (0, 0, 0)
            i_colour = (r_diff * i, g_diff * i, b_diff * i)
            self.set_colour(i_colour)
            time.sleep(slice_time)
        self.set_colour(new_colour)
        return new_colour

    def set_colour(self, colour: tuple):
        r = (colour[0] / 255) * 100
        g = (colour[1] / 255) * 100
        b = (colour[2] / 255) * 100
        self.pwm_red.ChangeDutyCycle(r)
        self.pwm_green.ChangeDutyCycle(g)
        self.pwm_blue.ChangeDutyCycle(b)

    def button_press(self):
        if self.state.value == len(State):
            self.state = State(1)
        else:
            self.state = State(self.state.value + 1)

        if self.state == State.STOPPED:
            self.set_colour((0, 0, 0))
            self.stop()
        if self.state.value == 1:
            self.start()

    def start(self):
        self.pwm_red.start(0)
        self.pwm_green.start(0)
        self.pwm_blue.start(0)

    def stop(self):
        self.pwm_red.stop()
        self.pwm_blue.stop()
        self.pwm_green.stop()

    def shutdown(self):
        self.stop()
        GPIO.cleanup()
