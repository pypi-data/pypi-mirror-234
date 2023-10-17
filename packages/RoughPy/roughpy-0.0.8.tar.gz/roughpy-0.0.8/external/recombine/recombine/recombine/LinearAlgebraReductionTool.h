//
// Created by sam on 20/06/22.
//

#ifndef RECOMBINE_LINEARALGEBRAREDUCTIONTOOL_H
#define RECOMBINE_LINEARALGEBRAREDUCTIONTOOL_H

#ifdef USE_FORTRAN_LAPACK
#include "lapack_fortran_definitions.h"
#else
#include "lapack_defns.h"
#endif

#ifndef REDUCTION_ALGO
#define REDUCTION_ALGO svd
#endif

namespace recombine {

class LinearAlgebraReductionTool {

    integer iNoCoords;
    integer iNoPoints;
    integer iNoRhs;
    VECTORD vdWork;
    VECTORI viWork;

    // counts the number of calls to the linear reduction package
    integer iNoCallsLinAlg;

public:
    enum MoveMass_type {
        svd,
        simplex
    };

    typedef void (LinearAlgebraReductionTool::*MoveMassFn_t)(VECTORD& eWeights, const VECTORD& ePoints,//VECTORD& eMassCog,
                                                             VECTORI& maxset);

private:
    MoveMass_type MoveMassAlgo;

public:
    LinearAlgebraReductionTool()
        : MoveMassAlgo(REDUCTION_ALGO),
          iNoCoords(1),
          iNoPoints(1),
          iNoRhs(1),
          iNoCallsLinAlg(0)
    {}

    inline integer INoCoords() const
    {
        return iNoCoords;
    }
    inline const integer& INoCoords(integer val)
    {
        return iNoCoords = val;
    }
    inline integer INoPoints() const
    {
        return iNoPoints;
    }
    inline const integer& INoPoints(integer val)
    {
        return iNoPoints = val;
    }
    inline index_integer INoCallsLinAlg() const
    {
        return iNoCallsLinAlg;
    }

    void MoveMass(VECTORD& eWeights, const VECTORD& ePoints,//VECTORD& eMassCog,
                  VECTORI& maxset);

private:
    void find_kernel(VECTORD A, integer rowsA, integer lda, VECTORD& K, integer rowsK, integer ldk);

    void MoveMass_svd(VECTORD& eWeights, const VECTORD& ePoints,//VECTORD& eMassCog,
                      VECTORI& maxset);

    void SharpenWeights(
            VECTORI& minset,
            VECTORI& maxset,
            const VECTORD& ePoints,
            VECTORD& eWeights,
            VECTORD Mcog);

#ifndef NOSIMPLEX
    void CLinearAlgebraReductionTool::MoveMass_simplex(VECTORD& eWeights, const VECTORD& ePoints,//VECTORD& eMassCog,
                                                       VECTORI& maxset);
#endif
};

}// namespace recombine

#endif//RECOMBINE_LINEARALGEBRAREDUCTIONTOOL_H
