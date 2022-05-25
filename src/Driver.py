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
    SERVO = 25


class MovementState(IntEnum):
    FORWARD = 0
    RIGHT = 3
    BREAKS = 1
    LEFT = 2


def init_igpiod(logger):
    # TODO: fer que s'executi al iniciar la raspberry
    """try:
        os.system('sudo killall pigpiod')
    except OSError:
        logger.warning('pigpiod not running')"""
    try:
        os.system('sudo pigpiod')
    except OSError:
        logger.warning("pigpiod already running")
    # avoiding jitter on servomotor
    Device.pin_factory = PiGPIOFactory()


class Driver:
    def __init__(self):
        # globals
        self.ACCELERATION_RATE = 0.5
        self.ACCELERATION = 10
        self.SPEED = 0
        self.MAX_SPEED = 100
        
        # logger
        self.logger = Logger().getLogger('Manual Driver', logging.DEBUG)
        init_igpiod(self.logger)
        
        # io management
        gpio.setmode(gpio.BCM)
        gpio.setup(Pins.DC_0, gpio.OUT)
        gpio.setup(Pins.DC_1, gpio.OUT)
        self.fw_pwm = gpio.PWM(Pins.DC_1, self.MAX_SPEED) # 100Hz
        self.fw_pwm.start(self.SPEED)
        self.servo = Servo(Pins.SERVO)
        self.last_action = None
        
        # accelerating timer
        self.fw_timer = threading.Timer(self.ACCELERATION_RATE, self.accelerate)

    def check_bit(self, value, bit):
        return (value & (1 << bit)) != 0
    
    def accelerate(self, acceleration_rate):
        if self.fw_timer is not None:
            self.fw_timer.cancel()
            
        self.fw_timer = threading.Timer(self.ACCELERATION_RATE, self.accelerate)
        self.fw_timer.start()
        if acceleration_rate > 0:
            self.SPEED = min(self.MAX_SPEED, self.SPEED + acceleration_rate)
            self.fw_pwm.ChangeDutyCycle(self.SPEED)
        else:
            self.SPEED = max(-self.MAX_SPEED, self.SPEED + acceleration_rate)
            self.fw_pwm.ChangeDutyCycle(self.SPEED)
        
        if abs(self.SPEED) >= self.MAX_SPEED:
            self.fw_timer.cancel()
            self.fw_timer = None
            
    def breaks(self, acceleration_rate):
        if self.fw_timer is not None:
            self.fw_timer.cancel()
        
        self.fw_timer = threading.Timer(self.ACCELERATION_RATE, self.accelerate)
        self.fw_timer.start()
        
        acceleration_rate = abs(acceleration_rate)
        if self.SPEED > 0:
            self.SPEED = max(0, self.SPEED - acceleration_rate)
            self.fw_pwm.ChangeDutyCycle(self.SPEED)
        elif self.SPEED < 0:
            self.SPEED = min(0, self.SPEED + acceleration_rate)
            self.fw_pwm.ChangeDutyCycle(self.SPEED)
        
        if abs(self.SPEED) == 0:
            self.fw_timer.cancel()
            self.fw_timer = None

            
    def apply_movement(self, metadata):
        if self.check_bit(metadata, MovementState.FORWARD):
            self.logger.debug('forward')
            gpio.output(Pins.DC_0, True)
            #gpio.output(Pins.DC_1, True)
            self.accelerate(self.ACCELERATION_RATE)
        elif self.check_bit(metadata, MovementState.BREAKS):
            self.logger.debug('breaks')
            if self.SPEED > 0:
                self.SPEED = -20
            self.accelerate(-(self.ACCELERATION_RATE))
            gpio.output(Pins.DC_0, False)
            #gpio.output(Pins.DC_1, True)
        else:
            self.fw_timer.cancel()
            self.logger.debug('rest power')
            gpio.output(Pins.DC_0, False)
            self.breaks(int(self.ACCELERATION_RATE/2))
                 
        if self.check_bit(metadata, MovementState.LEFT):
            self.logger.debug('left')
            self.servo.min()
        elif self.check_bit(metadata, MovementState.RIGHT):
            self.logger.debug('right')
            self.servo.max()
        else:
            self.logger.debug('rest steering')
            self.servo.mid()
            
        self.last_action = metadata
            
