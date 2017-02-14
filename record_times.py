#!/bin/python
import os
import csv
from datetime import datetime
from enum import Enum

# System-agnostic get-character method. See http://stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user
def _find_getch():
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch

    # POSIX system. Create and return a getch that manipulates the tty.
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch

getch = _find_getch()
dir_path = os.path.dirname(os.path.realpath(__file__))

INTRO_STR = """Starting collection. Controls:
<Enter>: Record someone entering 
<Space>: Record someone leaving
<Esc>: Stop collection and record data"""

CSV_HEADINGS = ['Timestamp', 'Direction']

ENTER_CHAR = '\r'
SPACE_CHAR = ' '
ESC_CHAR = '\x1b'

class Direction(Enum):
    IN = 'IN'
    OUT = 'OUT'

class Event():
    def __init__(self, time, direction):
        self.time = time
        self.direction = direction

    def __str__(self):
        return '%s at %s' % (self.direction.value, self.time.strftime("%I:%M:%S %p"))

def run_collection():
    print(INTRO_STR)
    start_time = datetime.now()

    fname = os.path.join(dir_path, 'data_%s.csv' % start_time.strftime('%m_%d_%y_%H_%M'))
    print('Writing collected data to %s...\n' % fname)
    with open(fname, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(CSV_HEADINGS)
        while True:
            command = getch()
            if command == ENTER_CHAR or command == SPACE_CHAR:
                direction = Direction.IN if command == ENTER_CHAR else direction.OUT
                time = datetime.now()
                event = Event(time,direction)
                print('Recorded ' + str(event))
                writer.writerow([str(time.time()), event.direction.value])
            elif command == ESC_CHAR:
                print('Received quit character, shutting down...')
                break
            


if __name__ == '__main__':
    run_collection()