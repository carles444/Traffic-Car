from time import sleep
from logger import Logger
import cv2 as cv


class AutonomousDriver:
    def __init__(self, driver):
        self.driver = driver
        self.logger = Logger().getLogger('AutonomousDriver')
        self.running = False
        self.camera = None
        
    def __del__(self):
        if self.camera is not None:
            self.camera.release()

    def setup(self):
        self.camera = cv.VideoCapture(0)
        if not self.camera.isOpened():
            self.logger.error('cannot initialize camera')
            self.running = False

    def stop_running(self):
        self.running = False

    def send_frame(self, frame):
        pass

    def __call__(self):
        self.running = True
        self.setup()
        print('running')
        while self.running:
            ret, frame = self.camera.read()
            if not ret:
                self.logger.error('cannot receive frame')
                break
            gray_im = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

