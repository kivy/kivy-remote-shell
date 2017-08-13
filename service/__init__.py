import kivy.utils
from kivy import platform as PLATFORM

try: # hack for Kivy pre-1.8
    PLATFORM = PLATFORM()
except TypeError:
    pass

if PLATFORM == 'android':
    import android
else:
    android = None

class ServiceAppMixin(object):
    def start_service(self, arg=''):
        if PLATFORM == 'android':
            self.service = android.AndroidService(title='Kivy Remote Shell', description='Twisted reactor running')
            self.service.start(arg) # accepts an argument, handled to PYTHON_SERVICE_ARGUMENT
            return True
        else:
            from multiprocessing import Process
            def _run_service(arg=arg):
                import os
                os.environ['PYTHON_SERVICE_ARGUMENT'] = arg
                import service.main
            self.service = Process(target=_run_service)
            self.service.start()
        return False

    def stop_service(self):
        if PLATFORM == 'android':
            self.service.stop()
            return True
        else:
            import os, signal
            os.kill(self.service.pid, signal.SIGKILL)
        return False
