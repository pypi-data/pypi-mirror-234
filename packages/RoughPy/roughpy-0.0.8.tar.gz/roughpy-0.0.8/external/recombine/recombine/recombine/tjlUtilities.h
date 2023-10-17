#ifndef tjlUtilities_h__
#define tjlUtilities_h__
#ifdef USE_FORTRAN_LAPACK
#include "lapack_fortran_definitions.h"// integer doublereal DGEMM
#else
#include "lapack_defns.h"
#endif
#include <algorithm> //std::min
#include <cassert>   //assert
#include <cstdint>   //uint32_t
#include <functional>//std::greater
#include <random>    // seed etc
#include <vector>    // vector

template<class T>
void fill_index_array(T& index_array)
{
    integer ii(0);
    for (auto& i : index_array) {
        i = ii++;
    }
};

// C = A * B
inline void multiply(VECTORD& C, integer ldc, integer rowsA, VECTORD& A, integer lda, VECTORD& B, integer ldb)
{
    integer rowsC;
    integer rows_opB, &columns_opA = rows_opB;
    integer columnsC, &columns_opB = columnsC;

    char layoutA('N'), layoutB('N');

    rowsC = rowsA;
    columns_opB = (integer)(end(B) - begin(B)) / ldb;
    columns_opA = (integer)(end(A) - begin(A)) / lda;

    doublereal alpha(1.), beta(0.);

    C.resize(ldc * columnsC);

    assert(rowsA <= lda && rowsA <= ldc && columns_opA <= ldb);
    /*
	void DGEMM(char* transa, char* transb, int* m, int* n, int* k, double* alpha, double* a, int
	* lda, double* b, int* ldb, double* beta, double* c, int* ldc);
	*/
    DGEMM(&layoutA, &layoutB, &rowsC, &columnsC, &rows_opB, &alpha,
          &A[0], &lda, &B[0], &ldb, &beta, &C[0], &ldc);
}

#pragma warning(disable : 4100)// rowsK is never used
inline void DFINDKERNEL(VECTORD A, integer rowsA, integer lda, VECTORD& K, integer rowsK, integer ldk)
{
    integer columnsA((integer)(end(A) - begin(A)) / lda);
    integer ldu(1);// don't return U
    VECTORD u(1);
    VECTORD s(std::min(rowsA, columnsA));
    integer ldvt(columnsA);
    VECTORD vt(ldvt * columnsA);
    VECTORD work(1);
    integer lwork(-1);
    integer info;
    if (lwork == -1) {
        DGESVD((char*)"N", (char*)"A", &rowsA, &columnsA, &A[0], &lda, &s[0], &u[0], &ldu, &vt[0], &ldvt, &work[0], &lwork, &info);
        work.resize(lwork = (integer)work[0]);
    }
    DGESVD((char*)"N", (char*)"A", &rowsA, &columnsA, &A[0], &lda, &s[0], &u[0], &ldu, &vt[0], &ldvt, &work[0], &lwork, &info);

    auto noNonzeroEV = std::upper_bound(begin(s), end(s), 10e-12, std::greater<doublereal>()) - begin(s);
    ////SHOW(s);
    ////SHOW(noNonzeroEV);
    K.resize(ldk * (columnsA - noNonzeroEV));
    for (ptrdiff_t i = noNonzeroEV; i < columnsA; ++i) {
        for (ptrdiff_t j = 0; j < columnsA; ++j) {
            K[j + (i - noNonzeroEV) * ldk] = vt[i + j * ldvt];
        }
    }
}

#endif// tjlUtilities_h__
