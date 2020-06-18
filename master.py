import numpy as np
import pickle as pk
import tod_picker
import tod_flats_anal
import flats_test



print("Master script for TOD processing with flats measurement")

filenm, basename, f_loic  = tod_picker.tod_pick()

print("from master: basename =  {}\n".format(basename))

f_flats_bad = tod_flats_anal.todFlats(basename, 0 )

print("f_flats_bad = \n {}  \n f_loic = {}\n".format( f_flats_bad,  f_loic ))
print("now to flats_test")


tp, tn, fn, fp = flats_test.fTest(f_flats_bad, f_loic)


print("pickle file {}".format(filenm))
print("TOD         {}".format(basename)) 

#print("tp = {}\ttn = {}\tfn = {}\tfp = {}\n".format(tp, tn, fn, fp))
fresults  = open("flats_bad_dict.pk", "rb")
ftp = open("tp_dict.pk", "rb")
ftn = open("tn_dict.pk", "rb")
ffn = open("fn_dict.pk", "rb")
ffp = open("fp_dict.pk", "rb")


flats_bad_dict    = pk.load(fresults)
tp_dict           = pk.load(ftp)
tn_dict           = pk.load(ftn)
fn_dict           = pk.load(ffn)
fp_dict           = pk.load(ffp)

fresults.close()
ftp.close()
ftn.close()
ffn.close()
ffp.close()

print("starting dictionary: flats_bad_dict = \n{}\n".format(flats_bad_dict))


flats_bad_dict[basename] = f_flats_bad
tp_dict[basename]        = tp
tn_dict[basename]        = tn
fn_dict[basename]        = fn
fp_dict[basename]        = fp

fresults  = open("flats_bad_dict.pk", "wb")
ftp = open("tp_dict.pk", "wb")
ftn = open("tn_dict.pk", "wb")
ffn = open("fn_dict.pk", "wb")
ffp = open("fp_dict.pk", "wb")


print("ending dictionary: flats_bad_dict = \n{}\n".format(flats_bad_dict))
pk.Pickler(fresults).dump(flats_bad_dict)
pk.Pickler(ftp).dump(tp_dict)
pk.Pickler(ftn).dump(tn_dict)
pk.Pickler(ffn).dump(fn_dict)
pk.Pickler(ffp).dump(fp_dict)

fresults.close()
ftp.close()
ftn.close()
ffn.close()
ffp.close()



print("tp_dict = {}\n\n".format(tp_dict))
print("tn_dict = {}\n\n".format(tn_dict))
print("fn_dict = {}\n\n".format(fn_dict))
print("fp_dict = {}\n\n".format(fp_dict))

print('end')




