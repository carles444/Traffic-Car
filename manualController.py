#import RPi.GPIO as gpio

class manualDriver:
    def __init__(self, comunication_socket):
        self.communication_socket = comunication_socket
        #gpio.setmode(gpio.BOARD)

        
    def __call__(self):
        data = self.sock.recv(1024).decode().lower()
        while data != 'exit':
            if data == 'power':
                pass
            elif data == 'break':
                pass
            elif data == 'right':
                pass
            elif data == 'left':
                pass
            data = self.sock.recv(1024).decode().lower()