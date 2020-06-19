# Flats_for_remote_use
Flats algorithm tailored to work on input of a single TOD's full path

Instructions:
   Run master_tod.py first.   Screen will prompt for the name of a TOD to be analyzed. Enter the full path name to the TOD.
   This might be streamlined to receive the TOD file name only, but only if moby2 can locate this file in the depot:
        /scratch/gpfs/snaess/actpol/tod/
        
   master_tod.py calls tod_flats_anal.py which utilizes the executable flatFull.so which was compiled from C code.
   
Output is entirely to the screen, and consists of a listing of the "bad" detectors according to the Flats algorithm plus a few other descriptives of this particular TOD.  

