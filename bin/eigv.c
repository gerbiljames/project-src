/*==========================================================
 * eigv.c  compute the smallest eigenvalues of a
 * real symmetric matrix
 *
 * The calling syntax is:
 *
 *		outMatrix = eigv(inMatrix,nEigenvals)
 *
 * Link with blas and lapack libraries, eg libmwblas and libmwlapack
 *========================================================*/

#include "mex.h"

/* Lapack header files */
#include "/usr/local/MATLAB/R2015a/extern/include/lapack.h"

char jobN='N';
#define JOBN &jobN
char jobU='U';
#define JOBU &jobU
char jobI='I';
#define JOBI &jobI

void eigv(double *Z, int n, int k,double* out)
{
	double* eigenvalue;
	double* workspace;
	double ev;
	ptrdiff_t i,idxl=1,idxu=k,num,lwork,info=0,cols=n,rows=n;
	double tol=1e-12;
	double d=0.0f;
	ptrdiff_t* iwork;
    
    eigenvalue=mxMalloc(n*sizeof(double));
	lwork=34*n;
    workspace=mxMalloc(2*lwork*sizeof(double));
    iwork=mxMalloc(2*5*cols*sizeof(ptrdiff_t));
	
	dsyevx(JOBN,JOBI,JOBU,&cols,Z,&rows,&d,&d,&idxl,&idxu,&tol,&num,eigenvalue,Z,&rows,workspace,&lwork,iwork,NULL,&info);

	mxFree(workspace);
	mxFree(iwork);

    for(i=0;i<k;i++)
        out[i]=eigenvalue[i];
	mxFree(eigenvalue);
}

void mexFunction( int nlhs, mxArray *plhs[],
                  int nrhs, const mxArray *prhs[])
{
    int n,k;
    double *Z;
    double *out;              /* output matrix */

    /* check for proper number of arguments */
    if(nrhs!=2) {
        mexErrMsgIdAndTxt("eigv:nrhs","Two inputs required.");
    }
    if(nlhs!=1) {
        mexErrMsgIdAndTxt("eigv:nlhs","One output required.");
    }
    
    /* make sure the first input argument is scalar */
    if( !mxIsDouble(prhs[0]) ) {
        mexErrMsgIdAndTxt("eigv:notDouble","Data type not handled.");
    }
    
    /* check that number of rows in second input argument is 1 */
    if(mxGetNumberOfElements(prhs[1])!=1 || !mxIsDouble(prhs[1])) {
        mexErrMsgIdAndTxt("eigv:notInteger","k must be an integer.");
    }
    
    Z = (double*)mxGetData(prhs[0]);
    k = (int)mxGetScalar(prhs[1]);
    n = (int)mxGetN(prhs[0]);

    plhs[0] = mxCreateDoubleMatrix(k,1,mxREAL);
    out = mxGetPr(plhs[0]);

    eigv(Z,n,k,out);
}
