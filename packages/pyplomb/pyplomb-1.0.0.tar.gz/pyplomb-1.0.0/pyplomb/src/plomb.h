/*
    LOMB-SCARGLE PERIODOGRAM
*/

#define PI   3.141592653589793115997963468544185161590576171875000
#define PI2  6.28318530717958623199592693708837032318115234375000
#define MACC 4

int plomb(double *x, double *y, const int n, double o, double hi, double *w1, double *w2, const int nw);
