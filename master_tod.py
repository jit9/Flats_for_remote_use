import numpy as np
import pickle as pk
#import tod_picker
import tod_flats_anal
#import flats_test

#   This script takes a full path name for a TOD and returns a list of those detectors which have
#   more than 40% of their TOD length as identically "flat"


print("Master script for TOD processing with flats measurement; one TOD at a time only")

basename = str(input("Enter full path to TOD basename   "))
print("\nbasename =  {}\n".format(basename))

f_flats_bad = tod_flats_anal.todFlats(basename)

print("number of detectors deemed bad by Flats =  {}".format(len(f_flats_bad)))

print("end")

