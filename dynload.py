import importlib
import os
import traceback
import sys
import inspect
import gc
from threading import Timer


def safe_run(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc(file=sys.stdout)
        print("^^^ safe run catch all traceback ^^^")


def safe_run_callback(func, fail_callback, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc(file=sys.stdout)
        print("^^^ safe run catch all traceback ^^^")
        if callable(fail_callback):
            fail_callback()


class FileWatch:
    def __init__(self, filename, callback=None):
        self._cached_stamp = 0
        self.filename = filename
        self.callback = None
        self.check()
        self.callback = callback

    def check(self):
        stamp = os.stat(self.filename).st_mtime
        if stamp != self._cached_stamp:
            self._cached_stamp = stamp
            if callable(self.callback):
                self.callback()


class Dynload:
    def __init__(self, module, manualCheck=False, checkInterval=1, qtimer=None, callback=None):
        self.module = module
        self.callback = callback
        self._watch = FileWatch(module.__file__, self.load)
        self.manualCheck = manualCheck
        self.checkInterval = checkInterval
        self.qtimer = qtimer
        if self.qtimer is not None:
            self.qtimer.timeout.connect(self.check)
            self.qtimer.start(checkInterval * 1000)
        elif not self.manualCheck:
            self.check()

    def check(self):
        self._watch.check()
        if not self.manualCheck and self.qtimer is None:
            Timer(self.checkInterval, self.check).start()

    def load(self):
        try:
            importlib.reload(self.module)
            clsmembers = [
                m
                for m in inspect.getmembers(self.module, inspect.isclass)
                if m[1].__module__ == self.module.__name__
            ]

            if len(clsmembers):
                # This method is quite slow. Try mixin https://stackoverflow.com/questions/328851/printing-all-instances-of-a-class
                for instance in gc.get_objects():
                    for clsmember in clsmembers:
                        if instance.__class__.__name__ == clsmember[0]:
                            instance.__class__ = clsmember[1]

        except:
            traceback.print_exc(file=sys.stdout)
            print("^^^ Dynload traceback ^^^")
        if callable(self.callback):
            self.callback()
