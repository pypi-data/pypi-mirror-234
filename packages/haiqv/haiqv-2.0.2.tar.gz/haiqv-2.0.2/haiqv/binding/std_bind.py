import os
import re
import sys
import signal
import time
from threading import Thread, Event


class StdBind:
    def __init__(self, log_name,  sleep_time, log_artifact):
        self._stdout = None
        self._stderr = None
        self._r = None
        self._w = None
        self._thread = None
        self._upload = None
        # self._active = False
        self._on_readline_cb = None
        self.log_name = log_name
        self.event = Event()
        self.event_for_handler = Event()
        self.sleep_time = sleep_time
        self.log_artifact = log_artifact
        self._started = False

    def _is_started(self):
        return self._started

    def _handler(self):
        while True:
            # if not self._active:
            if self.event_for_handler.is_set():
                break
            line = self._r.readline()
            if len(line) == 0:
                continue
            if re.sub('(\n|\r)$', '', line):
                with open(self.log_name, 'a', encoding='utf8') as f:
                    f.write(line)
            self._print(line)

    # def signal_handler(self, signum, frame):
    #     if signum == signal.SIGINT:
    #         self.stop_bind()
    #         # if os.path.isfile(self.log_name):
    #         #     os.remove(self.log_name)
    #         exit(1)
    #
    #     if signum == signal.SIGTERM:
    #         self.stop_bind()
    #         # if os.path.isfile(self.log_name):
    #         #     os.remove(self.log_name)
    #         exit(0)

    def batch_upload_log(self):
        _time = time.time()
        while True:
            if self.event.is_set():
                break
            if time.time() - _time >= self.sleep_time:
                if os.path.isfile(self.log_name):
                    self.log_artifact(self.log_name)
                _time = time.time()
            time.sleep(0.1)
        if os.path.isfile(self.log_name):
            os.remove(self.log_name)

    def _print(self, s, end=""):
        print(s, file=self._stdout, end=end)

    def start_bind(self):
        # if self._active:
        if self._started:
            return
        # self._active = True
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        r, w = os.pipe()
        r, w = os.fdopen(r, 'r'), os.fdopen(w, 'w', 1)
        self._r = r
        self._w = w
        sys.stdout = self._w
        sys.stderr = self._w
        # self._thread = Thread(target=self._handler)
        self._thread = Thread(target=self._handler, daemon=True)
        self._thread.start()
        self._started = True

    def stop_bind(self):
        # if not self._active:
        if not self._started:
            return
        # self._active = False
        self.event_for_handler.set()
        self.event.set()
        print('')
        if self._thread:
            self._thread.join()
        self._w.close()
        self._r.close()
        sys.stdout = self._stdout
        sys.stderr = self._stderr
        self._started = False
