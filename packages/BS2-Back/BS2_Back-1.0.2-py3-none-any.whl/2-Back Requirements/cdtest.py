import pyxid2
devices = pyxid2.get_xid_devices()
global dev
dev = devices [1]
import time
from datetime import datetime

def stimtest():
    
    for line_index in range(1, 13):
        dev.activate_line(lines=line_index)

    for line in range(1,2):
        dev.activate_line(lines = line)

    for line in range(2,3):
        dev.activate_line(lines = line)

    for line in range(3,4):
        dev.activate_line(lines = line)

    for line in range(4,5):
        dev.activate_line(lines = line)

    for line in range(5,6):
        dev.activate_line(lines = line)

    for line in range(6,7):
        dev.activate_line(lines = line)

    for line in range(7,8):
        dev.activate_line(lines = line)

    for line in range(8,9):
        dev.activate_line(lines = line)

    for line in range(9,10):
        dev.activate_line(lines = line)

    for line in range(10,11):
        dev.activate_line(lines = line)

def test1():
    print("Test Pulse 1")
    for line in range(4,5):
        dev.activate_line(lines = line)

def f():
    print("Test Pulse 2")
    for line in range(1,2):
        dev.activate_line(lines = line)

def j():
    print("Test Pulse 2")
    for line in range(3,4):
        dev.activate_line(lines = line)


def rt():
    print("RT")
    for line in range(1,2):
        dev.activate_line(lines = line)

    rttime = time.time()

def test():
    print("Test")
    for line in range(6,7):
        dev.activate_line(lines = line)

def linetest():
        print("Line Test")
        dev.activate_line(lines = 7)
