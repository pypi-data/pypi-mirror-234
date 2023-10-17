#!/usr/bin/env cpython
#
# PLOMB: LOMB-SCARGLE PERIODOGRAM
#
cimport cython
cimport numpy as np

import numpy as np

cdef extern from "plomb.h":
    cdef int c_plomb "plomb" (double *x, double *y, const int n, double o, double hi, double *w1, double *w2, const int nw)


@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
@cython.nonecheck(False)
@cython.cdivision(True)    # turn off zero division check
def cy_plomb(double[:] t, double[:] y, int ofac = 4, int hifac = 1):
    '''
    freq,psd = plomb(t,x) returns the Lomb-Scargle power spectral density (PSD) 
    estimate, pxx, of a signal, x, that is sampled at the instants specified in t. 
    t must increase monotonically but need not be uniformly spaced. 
    All elements of t must be nonnegative. pxx is evaluated at the frequencies 
    returned in f.
    '''
    # Defaults to match MATLAB's PLOMB
    cdef int nt = t.shape[0], nwk = nt*ofac*hifac*16, nout

    # Create output arrays
    cdef np.ndarray[np.double_t,ndim=1] freq = np.zeros((nwk,),np.double)
    cdef np.ndarray[np.double_t,ndim=1] psd  = np.zeros((nwk,),np.double)

    # Call C plomb function
    nout = c_plomb(&t[0],&y[0],nt,ofac,hifac,&freq[0],&psd[0],nwk)

    # Return cropped arrays
    return freq[1:nout], psd[1:nout]