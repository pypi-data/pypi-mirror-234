#ifndef lapack_fortran_definitions_h__
#define lapack_fortran_definitions_h__
#include <cstddef>
#include <map>
#include <vector>
/*
compiler & linker (for large array indexes - drop the I if all calls to lapack use (32 bit) int)

sequential
/DMKL_ILP64 -I%MKLROOT%/include
mkl_intel_ilp64.lib mkl_core.lib mkl_sequential.lib

multi-threaded
/DMKL_ILP64 /Qopenmp -I%MKLROOT%/include
mkl_intel_ilp64.lib mkl_core.lib mkl_intel_thread.lib (and for VS compiler libiomp5md.lib -ldl)

and for 32 bit simply don't define MKL_ILP64 and change mkl_intel_ilp64.lib to mkl_intel_c.lib
*/

//#include "mkl_types.h"
//typedef MKL_INT integer;

// Check windows
#if _WIN32 || _WIN64

#if _WIN64
#if !defined(MKL_ILP64) && !defined(MKL_LP64)
#define MKL_ILP64
#endif
#endif

#ifdef MKL_ILP64
#pragma comment(lib, "mkl_intel_ilp64.lib")
typedef ptrdiff_t integer;
typedef size_t index_integer;
#else
#ifdef _WIN64
#pragma comment(lib, "mkl_intel_lp64.lib")
typedef int integer;
typedef unsigned int index_integer;
#else
#pragma comment(lib, "mkl_intel_c.lib")
typedef ptrdiff_t integer;
typedef size_t index_integer;
#endif

#endif
#else
// Not windows - assume that lapack has 64 bit integers in 64 bit systems
typedef ptrdiff_t integer;
typedef size_t index_integer;
#endif

typedef double doublereal;

typedef std::vector<doublereal> VECTORD;
typedef std::vector<integer> VECTORI;
typedef VECTORD::const_iterator CONST_D_IT;
typedef VECTORD::iterator D_IT;
typedef VECTORI::const_iterator CONST_I_IT;
typedef VECTORI::iterator I_IT;

// Y=a*X+Y
extern "C" void DAXPY(integer* N, doublereal* A, doublereal* X, integer* INCX, doublereal* Y, integer* INCY);

extern "C" void DGEMM(char* transa, char* transb, integer* m, integer* n, integer* k, doublereal* alpha, doublereal* a, integer* lda, doublereal* b, integer* ldb, doublereal* beta, doublereal* c, integer* ldc);

extern "C" doublereal DASUM(integer* n, doublereal* x, integer* incx);

extern "C" integer IDAMAX(integer* n, doublereal* x, integer* incx);

extern "C" void DGELS(char* transa, integer* m, integer* n, integer* nrhs, doublereal* a, integer* lda, doublereal* b, integer* ldb,
                      doublereal* work, integer* lwork, integer* info);

extern "C" void DGELSS(integer* m, integer* n, integer* nrhs, doublereal* a, integer* lda, doublereal* b, integer* ldb,
                       doublereal*
                               s,
                       doublereal* rcond, integer* rank, doublereal* work, integer* lwork, integer* info);

extern "C" void DGESVD(char* jobu, char* jobvt, integer* m, integer* n, doublereal* a, integer* lda, doublereal* s, doublereal* u, integer* ldu, doublereal* vt, integer* ldvt, doublereal* work, integer* lwork, integer* info);

extern "C" void DGELSD(integer* m, integer* n, integer* nrhs, doublereal* a, integer* lda, doublereal* b, integer* ldb,
                       doublereal* s, doublereal* rcond, integer* rank, doublereal* work, integer* lwork, integer* iwork, integer* info);

#endif// lapack_fortran_definitions_h__
