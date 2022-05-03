from datetime import datetime
import logging

class Logger:
    def __init__(self):
        pass
    
    def getLogger(self, class_name, level):
        with open(class_name + '.log', 'a') as log_file:
            log_file.write('\n\n')
            log_file.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            log_file.write('\n\n')

        logger = logging.getLogger(class_name)
        logging.basicConfig(filename=class_name + '.log')
        logger.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter('%(asctime)s: %(name)s  [%(levelname)s]  %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger