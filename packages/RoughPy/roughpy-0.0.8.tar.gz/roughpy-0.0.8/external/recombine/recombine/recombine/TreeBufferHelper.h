/* Copyright -  All Rights Reserved - Terry Lyons 2008 */
#pragma once

#include <cstddef>
#ifdef USE_FORTRAN_LAPACK
#include "lapack_fortran_definitions.h"
#else
#include "lapack_defns.h"
#endif

struct CTreeBufferHelper {
    // the number of trees in the initial forest
    index_integer iNoTrees;
    // the number of leaves in the initial forest
    index_integer iInitialNoLeaves;
    // vdBuffer[iIndex +  iNoPointsToBeprocessed]
    // = vdBuffer[ 2 * iIndex ] + vdBuffer[ 2 * iIndex + 1 ] ;

    CTreeBufferHelper(index_integer SmallestReducibleSetSize, index_integer NoPointsToBeprocessed);
    bool isleaf(const index_integer& node) const;
    size_t end() const;
    bool isnode(const index_integer& node) const;
    size_t parent(const index_integer& node) const;
    bool isroot(const index_integer& node) const;
    size_t left(const index_integer& node) const;
    size_t right(const index_integer& node) const;
};
