#ifndef reweight_h__
#define reweight_h__
#include "tjlUtilities.h"
#include <algorithm>
#include <functional>
#include <math.h>
#include <vector>
#ifdef USE_FORTRAN_LAPACK
#include "lapack_fortran_definitions.h"
#else
#include "lapack_defns.h"
#endif
#include <deque>
#pragma warning(disable : 4100)
inline void reweight(
        I_IT rIDXb,//->an index of length rP for the rows in P and K
        I_IT cIDXb,//->an index of length cK for the columns in K
        D_IT P,    //->a positive measure on rP points with strictly positive mass at at least one of the points
        D_IT K,    //->cK independent real column vectors on the same rP points - given column by column - (and tested only in the case with sum over each row is 1)
        const integer rP,
        const integer ldk,// the stride in K
        const integer cK,
        const doublereal probability_zero_tolerance// UNUSED an empirical measure of the errors rounding gives to probability measure calculations
)
// on return K is triangular,
// P is a positive measure concentrated on only rP-cK points (a probability measure if the row-sums in K are zero)
// the support of P is [cK,rP) and rIDXb -> the associated permutation of rows
// the only changes to P (other than the permutation) are from adding linear multiples of rows in K
//
// so if A is a matrix with as many columns as P has rows and has K in its kernel the x := AP is not changed by this reduction process
// if A also has as its top row the constant value 1 then P out will have the same total mass on output as input.
// In its current form with rP = say 2000 and cK 1000 the computation sequentially takes approximately 1/3 the time that the DGESVD
// takes to do the svd that finds the kernel of A (T(2000,1000)). Using the tree structure it can therefore reduce the computation time by
// where previously it would have taken 1000 * T(1001,1000). Since T(2000,1000)/T(1001,1000) < ?6 we see around a 100 times speed up.
// on a single thread on Lenovo X201 laptop the reduction (including finding K) takes less than 8 seconds including lots of setup.
/*
	weight : 1

	weight : 1

	rank : 999

	Success: 1 tests passed.
	Test time: 7.64 seconds.
	Press any key to continue . . .
	*/
{
    const integer& rK = rP;

    D_IT Kb = K;
    D_IT Pb = P;
    const D_IT Ke = (Kb + ldk * cK);
    const D_IT Pe = (Pb + rP);

    //// zeros_in_P
    // Cannot update P without updating K to be zero on the zeros of P unless K is empty
    // so these zeros force a K update

    std::deque<integer> zeros_in_P;
    for (auto i = Pb; i != Pe; ++i)
        if (abs(*i) == 0.) zeros_in_P.push_front((integer)(&*i - &*Pb));

    // main loop
    for (integer O = 0; O < cK;) {
        D_IT oKb = (Kb + O * (ldk + 1)); // &K[indent,indent]
        D_IT oPb = (Pb + O);             // &P[indent]
        integer oCL(rK - O), oCN(cK - O);// offset column length and number of columns

        auto updateKincrementO = [rK, cK, oKb, oPb, ldk, Ke, oCL, oCN, &O, rIDXb, K](integer r) -> void {
            for (D_IT c = oKb; Ke - c >= ldk + oCL;) {
                assert(r >= 0);
                c += ldk;
                // rank one update - for each column c
                doublereal factor = -*(c + r) / *(oKb + r);
                ////////////////////////////
                if (!isnan(factor))
                // if *(oKb + r) is zero then *(c + r) should be too so no need to update or crash
                // if *(oKb + r) is nearly zero then the column pivoting and choosing the max
                // crucially ensures that factor is at most 1 otherwise chaos!! update as usual
                {
                    // remove complex references from within the loop to better optimize it
                    integer _oCL = oCL;
                    // outside the mkl code this is the most expensive part of the algorithm. The elemntary row operations can be vectorised
                    // but once this is done, the parallelism is very hard to capitalize as the algorithm limit seems to be bandwidth.
                    // however, there is a limited gain from to threads, the setup costs add 60% to the time taken
                    // but in clock time there is an acceleration
                    // maybe there is a gain to be had by widening the parallelism so thread startup can be better amortised
                        integer chunk_size = 512;
#pragma omp parallel for num_threads(2)
                    for (integer j = 0; j < _oCL; j += chunk_size) {
                        integer this_chunk_size = (j + chunk_size < _oCL) ? chunk_size : _oCL - j;
                        double* _c = &(*(c + j));
                        double* _oKb = &(*(oKb + j));
                        double _factor = factor;
                        integer _oCL2(this_chunk_size);
#pragma omp simd
                        for (integer jj = 0; jj < _oCL2; ++jj)
                            _c[jj] += _factor * _oKb[jj];
                    }
                }
                ////////////////////////////
                // "swap" entry in row 0 to row r and since the existing entry in row r is zero just set row 0 to zero
                if (r != 0)
                    *(c + r) = *c;
                *c = 0.;
            }
            // now deal with the modifying row at oKb and the probability at oPb
            if (r != 0) {
                *(oPb + r) = *oPb;
                *oPb = 0.;
                std::swap(*(oKb + r), *oKb);
                std::swap(rIDXb[r + O], rIDXb[O]);
            }

            // update the offset
            ++O;
        };

        // there will be situations where P has zeros and
        // in this case K still needs to be triangulated
        // so that further updates proceed correctly

        if (!zeros_in_P.empty()) {
            // now update K
            integer r = zeros_in_P.back() - O;
            zeros_in_P.pop_back();
            // find the column with the biggest value in the r'th slot (they may all be zero I suppose)
            D_IT found = oKb + r;
            if (oCN > 0)
                for (D_IT first = found; ldk < (Ke - first);) {
                    first += ldk;
                    assert(Ke - first >= (oCL - r));
                    if (abs(*first) > abs(*found)) found = first;
                }
            if (found != oKb + r) {
                // swap that column and the initial (0th) column
                std::swap_ranges(oKb, oKb + oCL, found - r);
                std::swap(cIDXb[(found - oKb) / ldk], cIDXb[0]);
            }
            updateKincrementO(r);
        }
        else {
            // make some zeros in P

            D_IT pfound = oPb;
            D_IT kfound = oKb;
            D_IT pfirst = pfound;
            D_IT kfirst = kfound;

            if (oCL > 0)
                for (; ++kfirst, ++pfirst < Pe;)
                    if (abs(*pfirst / (*kfirst)) < abs(*pfound / (*kfound))) {
                        pfound = pfirst;
                        kfound = kfirst;
                    }
            integer r = (integer)(kfound - oKb);
            // update P to have zero
            doublereal factor = -(*(pfound) / *(kfound));
            for (pfirst = oPb, kfirst = oKb; pfirst != Pe; ++pfirst, ++kfirst) {
                if (pfirst == oPb + r) *pfirst = 0.;
                else
                    *pfirst += (factor * (*kfirst));
                assert(*pfirst >= 0);
            }
            updateKincrementO(r);
            // TODO: THERE IS A PROBLEM IN THIS LOOP I THINK
            // IS IT EVALUATED and is oPb defined
            // check for additional zeros in (oPB, Pend)
            // use absolute addressing so that if there are multiple zeros addresses do not need to be updated as O changes
            for (auto i = oPb; (Pe - i) > 1;) {
                ++i;
                if (*i == 0.) zeros_in_P.push_front((integer)(&*i - &*Pb));
            }
        }
    }
}

#endif// reweight_h__
