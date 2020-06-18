import numpy as np
import pickle as pk

def tod_pick():


   print("This script reads a pickle file and produces a list of the sel values from that file as a .npy file")

## pickle file name (filenm) comes when this module is called from master.py
   filenm = input("Enter file to read  ")

   f = open(filenm, "rb")

   data = pk.load(f, encoding = "latin1")

   i = 0
   length = len(data['name'])
   print("length is  {}".format(length))

## TOD number is selected from master.py and comes with the call to this module

   basenumber = input("Enter TOD index number to select TOD:  ")
   basename   = str(data['name'][int(basenumber)])
   
   print("basename =  {}\n".format(basename))

   index_for_match = str("NO Match")
   i = 0
   while i < length:
      if data['name'][i] == basename :
         print("data element number is  {}".format(i))
         index_for_match = i
      i += 1

   sel_data = data['sel'].transpose()
   print("basename is  {}\tdata element number is {}\n".format(basename, index_for_match))
   sel = sel_data[index_for_match]
   print("shape of sel = {}\n".format(np.shape(sel)))
   np.save(basename+"_results.npy", sel)
   f.close()
   return filenm, basename, sel



