import os
import time
import sys
from threading import Thread


#输出unity导出工程的日志
class Tail(Thread):

    def __init__(self, filename):
        self._filename = filename
        self._stop_reading = False

        Thread.__init__(self)

    def run(self):
        while not os.path.exists(self._filename):
            time.sleep(0.1)
        with self.open_default_encoding(self._filename, mode='rb') as file:
            while True:
                where = file.tell()
                line = file.readline()
                if self._stop_reading and not line:
                    break
                if not line:
                    time.sleep(1)
                    file.seek(where)
                else:
                    if sys.stdout.closed:
                        return
                    print(line.rstrip())
                    sys.stdout.flush()

    def stop(self):
        self._stop_reading = True
        # Wait for thread read the remaining log after process quit in 5 seconds
        self.join(5)

    @staticmethod
    def open_default_encoding(file, mode):
        return open(file, mode=mode)
