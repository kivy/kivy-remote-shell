import os
import time

# get the argument passed
arg = os.getenv('PYTHON_SERVICE_ARGUMENT')

while True:
    # this will print PYTHON_SERVICE_ARGUMENT content continually, even when application is switched
    print arg
    #from snips import native_toast
    #native_toast(arg, True)
    time.sleep(3)
