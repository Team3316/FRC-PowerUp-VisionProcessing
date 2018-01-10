import logging
import os
import time

loggerFileName = (str(time.ctime()) + ".log").replace(" ", "_")

if not os.path.exists('/var/log/roboticsVision'):
    os.mkdir('/var/log/roboticsVision')

logging.basicConfig(filename='/var/log/roboticsVision/' + loggerFileName, level=logging.DEBUG)
logger = logging.getLogger()

# NOTE: every import of this module will create another instance of logger? if so who do i create a singleton class in Python?