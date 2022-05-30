import RPi.GPIO as gpio
from enum import IntEnum
from logger import *
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo, Device
import os
import threading

class Pins(IntEnum):
    DC_0 = 23
    DC_1 = 24
    SERVO = 18


class MovementState(IntEnum):
    FORWARD = 0
    RIGHT = 3
    BACKWARD = 1
    LEFT = 2
    POWER_REST = 5
    STEER_REST = 6
    BREAKS = 7


def init_pigpiod(logger):
    logger.debug('pigpio mode')
    os.system('sudo pigpiod')
    # avoiding jitter on servomotor
    Device.pin_factory = PiGPIOFactory()


class Driver:
    def __init__(self):
        # globals
        self.ACCELERATION_RATE = 0.5
        self.ACCELERATION = 10
        self.speed = 0
        self.MAX_SPEED = 100
        self.STEER_REST = 0
        self.MAX_STEER = 0.65
        
        # logger
        self.logger = Logger().getLogger('Manual Driver', logging.DEBUG)
        init_pigpiod(self.logger)
        
        # io management
        gpio.setmode(gpio.BCM)
        gpio.setup(Pins.DC_0, gpio.OUT)
        gpio.setup(Pins.DC_1, gpio.OUT)
        self.pwm = gpio.PWM(Pins.DC_1, self.MAX_SPEED)  # 100Hz
        self.pwm.start(self.speed)
        self.servo = Servo(Pins.SERVO)
        self.last_action = MovementState.POWER_REST
        
        # accelerating timer
        self.fw_timer = threading.Timer(self.ACCELERATION_RATE, self.accelerate, [0])
        self.bw_timer = threading.Timer(self.ACCELERATION_RATE, self.accelerate, [0])
        self.rst_timer = threading.Timer(self.ACCELERATION_RATE, self.accelerate, [0])

    def __del__(self):
        if self.fw_timer is not None:
            self.fw_timer.cancel()
        if self.bw_timer is not None:
            self.bw_timer.cancel()
        if self.rst_timer is not None:
            self.rst_timer.cancel()
        gpio.cleanup()

    def check_bit(self, value, bit):
        return (value & (1 << bit)) != 0
    
    def accelerate(self, acceleration):
        self.logger.debug(self.speed)
        if acceleration > 0:
            self.bw_timer.cancel()
            self.rst_timer.cancel()
            self.speed = min(self.MAX_SPEED, self.speed + acceleration)
            self.pwm.ChangeDutyCycle(abs(self.speed))
            if self.speed < self.MAX_SPEED:
                self.fw_timer = threading.Timer(self.ACCELERATION_RATE, self.accelerate, [acceleration])
                self.fw_timer.start()
        else:
            self.fw_timer.cancel()
            self.rst_timer.cancel()
            self.speed = max(-self.MAX_SPEED, self.speed + acceleration)
            self.pwm.ChangeDutyCycle(abs(self.speed))
            if abs(self.speed) < self.MAX_SPEED:
                self.bw_timer = threading.Timer(self.ACCELERATION_RATE, self.accelerate, [acceleration])
                self.bw_timer.start()
        gpio.output(Pins.DC_0, self.speed > 0)

    def breaks(self, acceleration):
        self.logger.debug(self.speed)
        self.fw_timer.cancel()
        self.bw_timer.cancel()
        acceleration = abs(acceleration)
        if self.speed > 0:
            self.speed = max(0, self.speed - acceleration)
            self.pwm.ChangeDutyCycle(self.speed)
        elif self.speed < 0:
            self.speed = min(0, self.speed + acceleration)
            self.pwm.ChangeDutyCycle(abs(self.speed))
        self.rst_timer = threading.Timer(self.ACCELERATION_RATE, self.breaks, [acceleration])

        self.rst_timer.start()

        if self.speed == 0:
            self.rst_timer.cancel()

    def apply_movement(self, metadata):
        if self.check_bit(metadata, MovementState.FORWARD):
            self.logger.debug('forward')
            if self.last_action != MovementState.BREAKS and self.speed < 0:
                self.breaks(self.acceleration)
                self.last_action = MovementState.BREAKS
            elif self.last_action != MovementState.FORWARD:
                self.accelerate(self.ACCELERATION)
                self.last_action = MovementState.FORWARD
        elif self.check_bit(metadata, MovementState.BACKWARD):
            self.logger.debug('breaks')
            if self.last_action != MovementState.BREAKS and self.speed > 0:
                self.breaks(-self.ACCELERATION)
                self.last_action = MovementState.BREAKS
            elif self.last_action != MovementState.BACKWARD:
                self.accelerate(-self.ACCELERATION)
                self.last_action = MovementState.BACKWARD
        else:
            self.logger.debug('rest power')
            if self.last_action != MovementState.POWER_REST:
                self.breaks(int(self.ACCELERATION / 2))
            self.last_action = MovementState.POWER_REST
            
        if self.check_bit(metadata, MovementState.LEFT):
            self.logger.debug('left')
            self.servo.value = self.MAX_STEER
        elif self.check_bit(metadata, MovementState.RIGHT):
            self.logger.debug('right')
            self.servo.value = -self.MAX_STEER
        else:
            self.logger.debug('rest steering')
            self.servo.value = self.STEER_REST

