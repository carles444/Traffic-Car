from time import sleep

class AutonomousDriver:
    def __init__(self, driver):
        self.driver = driver
    
    def stop_running(self):
        self.running = False
        
    def __call__(self):
        self.running = True
        print('running')
        while self.running:
            sleep(2)
            print('running')
        print('end')
        