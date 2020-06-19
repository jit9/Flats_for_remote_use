#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

double stdv(double data[], int length)
   {
        int i;
        double deviation, sum, sumsqr, mean, variance, stddeviation;
    
        sum = sumsqr = 0 ;
        for (i = 0; i < length; i++)
        {
            sum = sum + data[i]; 
        }
        mean = sum/(float)length;
        for (i = 1 ; i< length; i++)
        {
            deviation = data[i] - mean;
            sumsqr += (deviation * deviation);
        }
        variance = sumsqr/(float)length ;
        stddeviation = sqrt(variance) ;

        return stddeviation;
     }

double absoluteValue(double x)
   {
       if (x >= 0.00)
          {  return x; }
       if (x <  0.00)
          {  return -x; }
       return 1;
   }





int flats(int length, double *data)
{
    double sum = 0.0;
    double  bigger, smaller;
    double delta[length], output[length], smoothed[length];
    double variability, fq, dq, mean;
    int i,m, id;
    int icount = 0;



// First apply anti-glitch routine
//
    for (id = 1; id < length; id++)
      {
    bigger = data[id];
    smaller = data[id-1];
    delta[id] = bigger - smaller;
      }
     variability =  stdv(delta, length);

     for ( i = 5; i < length-5 ;  i++)
     {
     fq = absoluteValue(delta[i]);
     if (fq  > 2.0 * variability);
       {
           data[i] = 0.5 * (data[i-5] + data[i+5]);   
//   output[i] = 0.5 * (output[i-5] + output[i+5]);
       }
     }


// Apply anti-glitch routine a second time:
//
//
    for (id = 1; id < length; id++)
      {
        bigger = data[id];
        smaller = data[id-1];
        delta[id] = bigger - smaller;
      }
     variability =  stdv(delta, length);

     for ( i = 5; i < length-5 ;  i++)
      {
        fq = absoluteValue(delta[i]);
        if (fq  > 2.0 * variability);
          {
           data[i] = 0.5 * (data[i-5] + data[i+5]);
//   output[i] = 0.5 * (output[i-5] + output[i+5]);
          }
       }
//   change over to array smoothed for further computions
//
     for (i = 0; i < length; i++)
       {
          smoothed[i] = data[i];
       }

//  Compute mean so smoothed data can be computed normalized by mean
//
    for ( i = 0; i < length; i++)
      {
        sum = sum + *smoothed;
      }
    mean = sum / (double) length;

    for (i = 0; i < length ;  i++)
      { smoothed[i] = smoothed[i] / mean ;
      }
//
// Compute number of flat data sections (over 3 data points)
//
  for(i = 3; i < length; i++)
  {
   if (data[i] == data[i-1] & data[i] == data[i-2])
     { 
     icount++;
         }
   }
         return icount;        

}  
