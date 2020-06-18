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

## calculates % of TOD named basename that exhibits more than 40% of  
## TOD length as "flat" 
## Returns a list called bad_list of these detectors.

  
def todFlats(basename):


   lib             = cdll.LoadLibrary("./flatFull.so")
   fltmod          = lib.flats

   fltmod.argtypes = [ctypes.c_int, ctypes.c_void_p]
   fltmod.restypes = ctypes.c_double

   fb = get_filebase()

   filename = fb.filename_from_name(basename, single=True)

   tod = moby2.scripting.get_tod({'filename':filename})

   len = int(np.shape(tod.data)[1])
   loop = 1 
   print("length of tod = ", len) 
   med   = np.zeros(len)
   delta = np.zeros(len)
# find mean value;  normalize tod values to the mean.
   n_dets =  int(np.shape(tod.data)[0])
   print("number of detectors = {}\n".format(n_dets))
   loop = 1
   pct_flats = 0.0
   flat_count = {}
   bad_list = []
   while loop < n_dets:
      detector = loop
      data = tod.data[detector]
      arr = (ctypes.c_double * len)(*data)
      flat_count[detector] = fltmod(len, arr)
      pct_flats = 100.0* flat_count[detector] / len
      if (pct_flats > 40.0):  bad_list.append(detector)
      loop += 1

   print("\n\nBad Detectors by the flats algorithm \n\n" )
   print("{}".format( bad_list))



   return bad_list 	

