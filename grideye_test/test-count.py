import csv
import sys
import numpy
import os
import glob
from people_count import PeopleCounter

def main():
    if len(sys.argv) < 2:
        print "Usage ./test-count.py <directory_name>"

    #Change path 
    path = "/Users/karnmalik/Desktop/549/utility/grideye_test/"+sys.argv[1]+"/"

    calc_in_counts_array = []
    calc_out_counts_array = []
    actual_in_counts_array = []
    actual_out_counts_array = []

    for filename in glob.glob(os.path.join(path, '*.csv')):
        
        #change this for how you name your directory for the test files
        filename = filename[filename.find("apr14")::]
        print filename
        data = numpy.genfromtxt(filename, delimiter=",")
        counter = PeopleCounter()

        in_count = 0
        out_count = 0

        print "========================================"
        print "TEST CASE FOR ", filename
        print "========================================"

        for idx, frame in enumerate(data):
            if idx == 0:
                actual_in_count = frame[0]
                actual_in_counts_array.append(actual_in_count)
                actual_out_count = frame[1]
                actual_out_counts_array.append(actual_out_count)


            frame = frame.reshape((8,8))
            counter.new_frame(frame)

            (in_count, out_count) = counter.count_people(idx)

        calc_in_counts_array.append(in_count)
        calc_out_counts_array.append(out_count)

        print "========================================"
        print "Total In: %f |" % in_count, "Actual In Count: %f" % actual_in_count
        print "Total Out: %f |" % out_count, "Actual Out Count: %f" % actual_out_count
        print "========================================"

    average_calculated_in_count = numpy.mean(calc_in_counts_array)
    average_actual_in_count = numpy.mean(actual_in_counts_array)
    average_calculated_out_count = numpy.mean(calc_out_counts_array)
    average_actual_out_count = numpy.mean(actual_out_counts_array)

    print "============================================================"
    print "Average In Calculated Count: ", average_calculated_in_count
    print "Average In Actual Count: ", average_actual_in_count
    print "Accuracy for in count: ", average_calculated_in_count/average_actual_in_count * 100, "%"
    print "Average Out Calculated Count: ", average_calculated_out_count
    print "Average Out Actual Count: ", average_actual_out_count
    print "Accuracy for out count: ", average_calculated_out_count/average_actual_out_count * 100, "%"
    print "============================================================"


if __name__ == '__main__':
    main()