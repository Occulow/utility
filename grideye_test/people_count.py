import numpy
import math
import sys
from enum import Enum
import time
import matplotlib.pyplot as plt

GRID_SIZE = 8
BUFFER_SIZE = 7
TRIGGER_INDEX = BUFFER_SIZE / 2
TRIGGER_COLUMNS = [
    {
        "trigger_column": 2,
        "check_offset": 1,
    },
    {
        "trigger_column": 5,
        "check_offset": -1,
    },
]

TRIGGER_THRESHOLD = 20
MAX_THRESHOLD = 10

class Direction(Enum):
    IN = 0
    OUT = 1

def is_local_max(frame, row, col):
    current_max = frame[row][col]
    # Greater than (row+1, col), (row-1, col)
    if current_max < frame[row+1][col] or current_max < frame[row-1][col]:
        return False
    # Greater than (row, col+1), (row, col-1)
    if current_max < frame[row][col+1] or current_max < frame[row][col-1]:
        return False
    # Greater than (row+1, col+1), (row-1, col-1)
    if current_max < frame[row+1][col+1] or current_max < frame[row-1][col-1]:
        return False
    # Greater than (row+1, col-1), (row-1, col+1)
    if current_max < frame[row+1][col-1] or current_max < frame[row-1][col+1]:
        return False
    return True

class PeopleCounter():
    def __init__(self):
        self.frame_buffer = []
        self.in_count = 0
        self.out_count = 0
        self.counted = False

    ##
    ## @brief      Determines the direction of a person at trigger_col by
    ##             checking the given column offset
    ##
    ## @param      self         Object
    ## @param      frame_index  Index of frame to check for the a person
    ##                          initially
    ## @param      trigger_col  Column to check for a person
    ## @param      offset       Offset to determine movement
    ##
    ## @return     Direction(Enum) of the direction a person moved when detected
    ##             in this column. Returns None if no person was detected.
    ##
    def determine_direction(self, frame_index, trigger_col, offset):
        # Error checking
        if frame_index >= BUFFER_SIZE-1 or frame_index < 1:
            raise Exception("Frame index must be in [1:BUFFER_SIZE-1] to \
                allow for past/future: %d" % frame_index)
        if trigger_col + offset < 0 or trigger_col + offset >= GRID_SIZE:
            raise Exception("trigger_col + offset is out of bounds: \
                (%d, %d)" % (trigger_col, offset))

        check_col = trigger_col + offset
        max_idx = self.frame_buffer[frame_index][:, trigger_col].argmax()
        current_max = self.frame_buffer[frame_index][max_idx][trigger_col]

        if current_max >= TRIGGER_THRESHOLD and is_local_max(self.frame_buffer[frame_index], max_idx, trigger_col):
            print "Trigger Max %d: %d" % (trigger_col, current_max)
            # Check check_col in the past
            # (Change upper bound to look further into the past)
            for i in range(1,2):
                past_frame = self.frame_buffer[frame_index - i]
                # Check for IN
                past_max_idx = past_frame[:, check_col].argmax()
                past_max = past_frame[past_max_idx][check_col]
                if math.fabs(past_max - current_max) <= MAX_THRESHOLD and is_local_max(past_frame, past_max_idx, check_col):
                    print "trig: %d, current_max: %d, past_max: %d" % (check_col, current_max, past_max)
                    print "Current"
                    print self.frame_buffer[frame_index]
                    print "Past"
                    print past_frame
                    if offset < 0:
                        return Direction.IN
                    elif offset > 0:
                        return Direction.OUT

            # Check check_col in the future 
            # (Change upper bound to look further into the future)
            for i in range(1,2):
                future_frame = self.frame_buffer[frame_index + i]
                future_max_idx = future_frame[:, check_col].argmax()
                future_max = future_frame[future_max_idx][check_col]
                if math.fabs(future_max - current_max) <= MAX_THRESHOLD and is_local_max(future_frame, future_max_idx, check_col):
                    print "trig: %d, current_max: %d, future_max: %d" % (check_col, current_max, future_max)
                    print "Current"
                    print self.frame_buffer[frame_index]
                    print "Future"
                    print future_frame
                    if offset < 0:
                        return Direction.OUT
                    elif offset > 0:
                        return Direction.IN
        return None

    def new_frame(self, processed_frame):
        # Add frame to buffer and cap buffer at BUFFER_SIZE
        self.frame_buffer.append(processed_frame)
        if len(self.frame_buffer) > BUFFER_SIZE:
            self.frame_buffer.pop(0)
        self.counted = False  

    def get_trigger_frame(self):
        if len(self.frame_buffer) < BUFFER_SIZE:
            return numpy.zeros((8,8))
        return self.frame_buffer[TRIGGER_INDEX]    

    ##
    ## @brief      Counts the number of people
    ##
    ## @param      self  Object
    ##
    ## @return     (Number of people in, Number of people out)
    ##
    def count_people(self):
        if len(self.frame_buffer) < BUFFER_SIZE:
            return (0,0)
        
        if self.counted:
            return (self.in_count, self.out_count)

        for trig in TRIGGER_COLUMNS:
            trigger_col = trig["trigger_column"]
            offset = trig["check_offset"]
            movement_dir = self.determine_direction(TRIGGER_INDEX, 
                trigger_col, offset)
            if movement_dir == Direction.IN:
                self.in_count += 0.5
            elif movement_dir == Direction.OUT:
                self.out_count += 0.5

        self.counted = True
        return (self.in_count, self.out_count)


def main():
    if len(sys.argv) < 2:
        print "Usage ./people_count.py <csv_file_name>"

    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.imshow(numpy.zeros((8,8)), cmap="hot", interpolation="none")
    im.set_clim(0,40)
    plt.show(block=False)

    # Show heatmap frame by frame, redrawing every 0.1 seconds (10 FPS)
    SLEEP_TIME = 0.1

    data = numpy.genfromtxt(sys.argv[1], delimiter=",")
    counter = PeopleCounter()

    in_count = 0
    out_count = 0

    for idx, frame in enumerate(data):
        if idx == 0:
            continue  # Skip invalid first frame
        # Adjust for old median files
        frame = frame.reshape((8,8)) * 4

        counter.new_frame(frame)
        old_in, old_out = (in_count, out_count)
        (in_count, out_count) = counter.count_people()
        if old_in != in_count or old_out != out_count:
            timestamp = idx / 10.0
            print "Frame %d [%.1fs]: (%f, %f)" % (idx, timestamp, 
                in_count, out_count)

        # Show frame
        im.set_array(counter.get_trigger_frame())
        fig.canvas.draw()

        time.sleep(SLEEP_TIME)

    print "========================================"
    print "Total In: %f" % in_count
    print "Total Out: %f" % out_count
    print "========================================"


if __name__ == '__main__':
    main()
