#include "lapack_defns.h"// index_integer double_real
#include "recombine.h"   //sRecombineInterface
#include "stdafx.h"
#include <algorithm>
#include <cassert>
#include <cmath>
#include <valarray>

namespace compare {

index_integer InsertLeafData(sRecombineInterface& data, std::valarray<doublereal>& vdArrayPointsBuffer, VECTORD& vdWeightsBuffer)
{
    void*& LocationBufIn = (data.pInCloud)->LocationBuf;
    index_integer NPointsIn = (data.pInCloud)->NoActiveWeightsLocations;
    vdArrayPointsBuffer.resize(2 * NPointsIn * data.degree, std::nan("a non number"));
    vdWeightsBuffer.resize(2 * NPointsIn, std::nan("a non number"));

    // Buffers large enough for any encompassing tree + 1 unused

    expander PointsToVectorDoubles = &(*data.fn);
    CConditionedBufferHelper arg3;
    arg3.NoPointsToBeprocessed = NPointsIn;
    arg3.SmallestReducibleSetSize = data.degree + 1;//legacy reasons
    arg3.pvCConditioning = (*data.pInCloud).end;
    PointsToVectorDoubles(LocationBufIn, &vdArrayPointsBuffer[0], &arg3);

    doublereal* WeightBufIn = (data.pInCloud)->WeightBuf;
    std::copy(WeightBufIn, WeightBufIn + NPointsIn, vdWeightsBuffer.begin());

    return NPointsIn;
}
};// namespace compare

doublereal RECOMBINE_API Compare(void* pData)
{
    // unpack the void pointer
    sRecombineInterface& data = *(sRecombineInterface*)pData;

    // expand and insert incoming leaf data into buffers
    std::valarray<doublereal> vdFlatPointsBuffer;
    VECTORD vdWeightsBuffer;
    index_integer NPointsIn = compare::InsertLeafData(data, vdFlatPointsBuffer, vdWeightsBuffer);
    assert(2 * NPointsIn == vdWeightsBuffer.size());

    // Identify the width of DATA (including the leading 1)
    index_integer Degree = vdFlatPointsBuffer.size() / vdWeightsBuffer.size();
    assert(data.degree == Degree);

    // reference the locations used for the outgoing data
    index_integer& NLocationsKept = (data.pOutCloudInfo)->No_KeptLocations;// number actually returned
    doublereal*& WeightBufOut = (data.pOutCloudInfo)->NewWeightBuf;        // an external buffer containing the weights of the kept Locations // capacity must be at least iNoDimensionsToCubature + 1
    index_integer*& LocationsKept = (data.pOutCloudInfo)->KeptLocations;   // an external buffer containing the offsets of the kept Locations // capacity must be at least iNoDimensionsToCubature + 1

    ///////////////////////////////////////////////////////////////////////////////////////////////
    // INIT FINISHED //
    ///////////////////////////////////////////////////////////////////////////////////////////////

    std::valarray<doublereal> init_cog(0., Degree), temp(0., Degree);
    for (index_integer i = 0; i < NPointsIn; i++) {
        std::slice vaSlice(Degree * i, Degree, 1);
        init_cog += (temp = vdFlatPointsBuffer[vaSlice]) * vdWeightsBuffer[i];
    }

    std::valarray<doublereal> final_cog(0., Degree), temp1(0., Degree);
    for (index_integer i = 0; i < NLocationsKept; i++) {
        std::slice vaSlice(Degree * LocationsKept[i], Degree, 1);
        final_cog += (temp = vdFlatPointsBuffer[vaSlice]) * WeightBufOut[i];
    }

    std::valarray<doublereal> error(init_cog - final_cog);
    return std::max(error.max(), -error.min());//worst case analysis
}
