import matplotlib as mpl
import matplotlib.pyplot as plt
import moby2
import pickle as pk
import math
import numpy as np
import moby2.scripting
from moby2.scripting import products
from moby2.tod.filter import prefilter_tod
from moby2 import libactpol
from moby2 import detectors
from scipy import stats
import time
import moby2.util
from moby2.scripting import get_filebase
from moby2 import instruments 
from moby2.instruments import actpol
import pandas
from pandas import DataFrame, Series
import ctypes
from ctypes import *
from ctypes import cdll
from numpy.ctypeslib import ndpointer



def antiglitch(input):
    i = 5
    output = input
    length = np.shape(input)[0]
    id = 5
    while id < length:
        delta[id] = input[id] - input[id-1]
        id += 1
    variability = np.std(delta)
    while i < length - 5:
        if abs(delta[i] ) > 2.0 * variability: 
            output[i] = .5*(input[i-5] + input[i+5])
#            print " outlier !   i = ", i, " value = ", input[i], " output = ", output[i]
        i += 1
    return output



#lib  = cdll.LoadLibrary("./flat.so")
#fltmod = lib.flatc
lib             = cdll.LoadLibrary("./flatFull.so")
fltmod          = lib.flats

fltmod.argtypes = [ctypes.c_int, ctypes.c_void_p]
fltmod.restypes = ctypes.c_double

#libGlitch = cdll.LoadLibrary("./glitch.so")
#glitchMod  = libGlitch.antiGlitch
#glitchMod.argtypes = [ctypes.c_int, ctypes.c_void_p]
#glitchMod.restypes = ctypes.c_double




t_start = time.time()
fb = get_filebase()

#basename = '1479923360.1484392604.ar4'
#basename = '1381820839.1381820862.ar1'

#basename ='1406162765.1406910436.ar2'
#basename = '1462279585.1462308129.ar3'
#basename = '1461123102.1461149098.ar3'
#basename = "1461044679.1461074472.ar3"
#basename = "1452671918.1452708770.ar3"
#basename = "1444794761.1444829875.ar3"
#basename = "1451240695.1451267738.ar3"
#basename = "1448662652.1448696742.ar3"

#basename =  "1451240695.1451267738.ar3"
#basename = "1451240695.1451267738.ar3"
#basename  =  "1443250367.1443285463.ar3"
basename = input("Enter TOD number with array")
pt =  int(input("Do you want to plot?  1=yes  2=no"))
filename = fb.filename_from_name(basename, single=True)

print("filename " , filename)

tod = moby2.scripting.get_tod({'filename':filename})

length = int(np.shape(tod.data)[1])
loop = 1 
print("length of tod = ", length) 
med   = np.zeros(length)
delta = np.zeros(length)
# find mean value;  normalize tod values to the mean.
n_dets =  int(np.shape(tod.data)[0])
print("number of detectors = {}\n".format(n_dets))
loop = 1
pct_flats = 0.0
flat_count = {}
bad_list = []


tesList = np.where(tod.info.array_data['det_type'] == 'tes')[0]
np.save("tesList.npy", tesList)


while loop < n_dets:
      if (loop % 100 == 0 ): print("detector number {}".format(loop))
      detector = loop
      data = tod.data[detector]

##      smoothed1 = antiglitch(tod.data[detector])
##  Perform a second anti-glitch -- this may help glitches
##      smoothed  = antiglitch(smoothed1) 
##  Use c module for antiGlitch:
##
#      arr1      = (ctypes.c_double * len)(*tod.data[detector])
#      smoothed  = glitchMod(len,arr1)
#      print("got to end of glitchMod")
#      print("type(smoothed) = {}\n".format(type(smoothed)))
##      mean = np.mean(smoothed)
##      smoothed = smoothed/mean

      if pt==1:
            plt.plot(data)
            plt.title(basename +"_raw(noSmoothing)_"  + "Detector "+str(detector))
            plt.savefig(basename+"_det_"+str(detector)+".png")
            plt.show()

      arr = (ctypes.c_double * length)(*data)

      flat_count[detector] = fltmod(length, arr)

      pct_flats = 100.0* flat_count[detector] / length
#      print("pct_flats for detector {}\t = {}".format(detector, pct_flats))
      if (pct_flats > 40.0):  bad_list.append(detector)
      loop += 1


print(basename+"\n{}".format( bad_list))
#print("flat count: \n\n{}".format(flat_count))

t_end = time.time()

print("elapsed time = {} sec. \n".format(t_end-t_start))
bad = open(basename+"_badList_>40.pk", "wb")
pk.dump(bad_list, bad)
bad.close()
S = Series(data = flat_count)

p = open(basename+"_flats.pk", "wb")
pk.dump(S, p)
p.close()


length_badList = len(bad_list)
print("length of badList = {}".format(length_badList))
pct_bad = round(length_badList*100.0/n_dets, 1)

print("Percent flats by detector > 40% = {} %".format(pct_bad))

print('end')

 	

