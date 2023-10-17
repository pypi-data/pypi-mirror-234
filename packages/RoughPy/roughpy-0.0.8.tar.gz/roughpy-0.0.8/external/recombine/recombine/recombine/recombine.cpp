// recombine.cpp : Defines the entry point for the DLL application.
//

#include <cassert>
#include <recombine.h>

#include "stdafx.h"
// Windows Header Files:
#ifndef NOMINMAX
#define NOMINMAX
#endif
#ifdef _WIN32
#include <windows.h>
#pragma warning(disable : 4100)
BOOL APIENTRY DllMain(HANDLE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)
{
    switch (ul_reason_for_call) {
    case DLL_PROCESS_ATTACH:
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}
#endif

#include "LinearAlgebraReductionTool.h"
#include "TreeBufferHelper.h"

using std::max;
using std::min;

namespace recombine04 {
//integer iNoCoords=2; //M
//integer iNoPoints=3; //N
integer iNoRhs = 1;//NRHS
// following not constant because the lapack programmes can change them (but dont....)
integer iOne(1);
integer iZero(0);
doublereal dOne(1);
doublereal dMOne(-1);
doublereal dZero(0);
char charN('N');

void ForestOfWeightedVectorsFromWeightedLeafVectors(const CTreeBufferHelper& bhBufInfo,
                                                    VECTORD& vdWeightsBuffer,
                                                    std::vector<std::valarray<doublereal>>& vdPointsBuffer);

void RepackPointBuffer(std::map<integer, ptrdiff_t>& currentroots,
                       std::map<index_integer, index_integer>& miTreePosition, VECTORD& weights, VECTORD& points,
                       index_integer pointdimension);

index_integer IdentifyLocationsRemainingAndTheirNewWeights(
        index_integer Degree,
        CTreeBufferHelper& bhBufInfo,
        std::map<index_integer, index_integer>& miTreePosition,
        VECTORD& vdWeightsBuffer,
        std::vector<std::valarray<doublereal>>& vdPointsBuffer,
        VECTORD& weights,
        index_integer& ICountCalls);

index_integer InsertLeafData(sRecombineInterface& data, std::valarray<doublereal>& vdArrayPointsBuffer,
                             VECTORD& vdWeightsBuffer);

}// namespace recombine04

void Recombine(void* pData)
{
    // unpack the void pointer
    sRecombineInterface& data = *(sRecombineInterface*)pData;

    // expand and insert incoming leaf data into buffers
    std::valarray<doublereal> vdFlatPointsBuffer;
    // InsertLeafData assigns memory: 2 * NPointsIn * data.degree
    // make this a memory mapped file
    VECTORD vdWeightsBuffer;
    //
    index_integer NPointsIn = recombine04::InsertLeafData(data, vdFlatPointsBuffer, vdWeightsBuffer);
    //
    //
    // Fix the width of DATA (including the leading 1)
    index_integer Degree = vdFlatPointsBuffer.size() / vdWeightsBuffer.size();
    assert(data.degree == Degree);

    // reference the locations used for the outgoing data
    index_integer& NLocationsKept = (data.pOutCloudInfo)->No_KeptLocations;// number actually returned
    doublereal*& WeightBufOut = (data.pOutCloudInfo)
                                        ->NewWeightBuf;// an external buffer containing the weights of the kept Locations // capacity must be at least iNoDimensionsToCubature + 1
    index_integer*& LocationsKept = (data.pOutCloudInfo)
                                            ->KeptLocations;// an external buffer containing the offsets of the kept Locations // capacity must be at least iNoDimensionsToCubature + 1

    ///////////////////////////////////////////////////////////////////////////////////////////////
    // INIT FINISHED //
    ///////////////////////////////////////////////////////////////////////////////////////////////
    ///////// Degree is the max number of of non-degenerate points

    //index_integer MaxPoints = Degree + 3;
    //if ( 7 >= NPointsIn )

    // TODO DONT CRASH when rhs is 2*degree
    index_integer MaxPoints = 2 * Degree;

    if (1 >= NPointsIn) {
        doublereal* pwOut = WeightBufOut;
        index_integer* pl = LocationsKept;
        NLocationsKept = NPointsIn;
        for (index_integer iIndex = 0; iIndex < NPointsIn; iIndex++) {
            *(pwOut++) = vdWeightsBuffer[iIndex];
            *(pl++) = iIndex;
        }
    }
    else {

        index_integer InitialNoTreesInForest(min(MaxPoints, NPointsIn));
        CTreeBufferHelper bhBufInfo(InitialNoTreesInForest, NPointsIn);

        // BAD UNNECCESARY COPY AND MEMORY USE HERE but tricky to remove
        // map buffer to array of val arrays for compatibility reasons
        std::vector<std::valarray<doublereal>>
                vdPointsBuffer(
                        bhBufInfo.end(), std::valarray<doublereal>(std::nan("value not yet assigned"), Degree));
        // populate the leaves

        for (index_integer i = 0; i < bhBufInfo.iInitialNoLeaves; i++) {
            std::slice vaSlice(Degree * i, Degree, 1);
            vdPointsBuffer[i] = vdFlatPointsBuffer[vaSlice];
        }

        // now fill the forest using the leafs, leaving exactly iNoTrees roots
        recombine04::ForestOfWeightedVectorsFromWeightedLeafVectors(bhBufInfo,
                                                                    vdWeightsBuffer,
                                                                    vdPointsBuffer);
        index_integer ICountCalls;
        std::map<index_integer, index_integer> miTreePosition;
        VECTORD weights;
        //SHOW(NPointsIn);
        ICountCalls = recombine04::IdentifyLocationsRemainingAndTheirNewWeights(
                Degree,
                bhBufInfo,
                miTreePosition,
                vdWeightsBuffer,
                vdPointsBuffer,
                weights,
                ICountCalls);
        doublereal* pw = WeightBufOut;
        index_integer* pl = LocationsKept;
        NLocationsKept = miTreePosition.size();//not weights.size();

        for (auto it = miTreePosition.begin(); it != miTreePosition.end(); ++it) {
            assert(bhBufInfo.isleaf(it->first));
            *(pw++) = weights[it->second];
            *(pl++) = it->first;
        }
        //(index_integer iIndex = 0; bhBufInfo.isleaf(iIndex); iIndex++)
    }
}

namespace recombine04 {

void ForestOfWeightedVectorsFromWeightedLeafVectors(const CTreeBufferHelper& bhBufInfo,
                                                    VECTORD& vdWeightsBuffer,
                                                    std::vector<std::valarray<doublereal>>& vdPointsBuffer)
{
    // create correct initial length and allocate memory for recipient valarrays
    // since slice cannot deduce it
    //// TODO
    //// optimise the OMP so it is faster than the non omp!!
#if 1
    {
        for (index_integer iIndex = bhBufInfo.iInitialNoLeaves; iIndex < bhBufInfo.end(); iIndex++) {
            index_integer uiLeftParent = bhBufInfo.left(iIndex);
            index_integer uiRightParent = bhBufInfo.right(iIndex);
            doublereal left = vdWeightsBuffer[uiLeftParent];
            doublereal right = vdWeightsBuffer[uiRightParent];
            doublereal sum = left + right;
            vdWeightsBuffer[iIndex] = sum;
            std::valarray<doublereal>& dPointsBuffer = vdPointsBuffer[iIndex];
            if (left <= right)
                dPointsBuffer = vdPointsBuffer[uiLeftParent] * (left / sum) + vdPointsBuffer[uiRightParent] * (1 - (left / sum));
            else
                dPointsBuffer = vdPointsBuffer[uiLeftParent] * (1 - (right / sum)) + vdPointsBuffer[uiRightParent] * (right / sum);
        }
    }
#else
    {
        const size_t sz = vdPointsBuffer[0].size(), blocksz(64);
        //#pragma omp parallel for
        for (size_t i = 0; i < sz; i += blocksz)
            for (index_integer iIndex = bhBufInfo.iInitialNoLeaves; iIndex < bhBufInfo.end(); iIndex++) {
                std::slice identity(i, std::min(sz, i + blocksz) - i, 1);
                index_integer uiLeftParent = bhBufInfo.left(iIndex);
                index_integer uiRightParent = bhBufInfo.right(iIndex);
                doublereal left = vdWeightsBuffer[uiLeftParent];
                doublereal right = vdWeightsBuffer[uiRightParent];
                doublereal sum = left + right;
                vdWeightsBuffer[iIndex] = sum;
                std::valarray<doublereal>& dPointsBuffer = vdPointsBuffer[iIndex];
                if (left <= right)
                    dPointsBuffer[identity] = std::valarray<doublereal>(vdPointsBuffer[uiLeftParent][identity]) * (left / sum) + std::valarray<doublereal>(vdPointsBuffer[uiRightParent][identity]) * (1 - (left / sum));
                else
                    dPointsBuffer[identity] = std::valarray<doublereal>(vdPointsBuffer[uiLeftParent][identity]) * (1 - (right / sum)) + std::valarray<doublereal>(vdPointsBuffer[uiRightParent][identity]) * (right / sum);
            }
    }

#endif
}

void RepackPointBuffer(std::map<integer, ptrdiff_t>& currentroots,
                       std::map<index_integer, index_integer>& miTreePosition, VECTORD& weights, VECTORD& points,
                       index_integer pointdimension)
{
    std::map<integer, ptrdiff_t> currentrootsnew;
    std::map<index_integer, index_integer> miTreePositionNew;
    VECTORD weightsnew(currentroots.size());
    VECTORD pointsnew(currentroots.size() * pointdimension);

    integer i = 0;
    auto itcurrrts = currentroots.begin();
    for (; itcurrrts != currentroots.end(); ++i, ++itcurrrts) {
        miTreePositionNew[itcurrrts->second] = i;
        currentrootsnew[i] = itcurrrts->second;
        weightsnew[i] = weights[itcurrrts->first];
        for (index_integer iM = 0; iM < pointdimension; iM++)
            pointsnew[i * pointdimension + iM] = points[itcurrrts->first * pointdimension + iM];
    }
    points.swap(pointsnew);
    weights.swap(weightsnew);
    currentroots.swap(currentrootsnew);
    miTreePosition.swap(miTreePositionNew);
}

index_integer IdentifyLocationsRemainingAndTheirNewWeights(
        index_integer Degree,
        CTreeBufferHelper& bhBufInfo,
        std::map<index_integer, index_integer>& miTreePosition,
        VECTORD& vdWeightsBuffer,
        std::vector<std::valarray<doublereal>>& vdPointsBuffer,
        VECTORD& weights,
        index_integer& ICountCalls)
{
    /////////////////////////////////////////////////
    //SHOW(vdWeightsBuffer.size());
    //SHOW(vdPointsBuffer.size());

    weights.clear();
    weights.resize(bhBufInfo.iNoTrees);
    // create local buffers
    VECTORD points(bhBufInfo.iNoTrees * Degree);
    std::map<integer, ptrdiff_t> currentroots;// (bhBufInfo.iNoTrees);
    VECTORI maxset;

    bool SomeLinearAlgebraToDo = true;// (bhBufInfo.end() >= bhBufInfo.iNoTrees);
    //assert(SomeLinearAlgebraToDo);

    for (index_integer iTreeIndexInFixedBuffer = 0;
         iTreeIndexInFixedBuffer < bhBufInfo.iNoTrees;
         iTreeIndexInFixedBuffer++) {
        ptrdiff_t currentroot = currentroots[iTreeIndexInFixedBuffer] = iTreeIndexInFixedBuffer + bhBufInfo.end() - bhBufInfo.iNoTrees;
        miTreePosition[(index_integer)currentroot] = iTreeIndexInFixedBuffer;
        weights[iTreeIndexInFixedBuffer] = vdWeightsBuffer[currentroot];
        for (index_integer iM = 0; iM < Degree; iM++)
            points[iTreeIndexInFixedBuffer * Degree + iM] = (vdPointsBuffer[currentroot])[iM];
    }

    //SHOW(miTreePosition.size());
    //SHOW(weights.size());

    recombine::LinearAlgebraReductionTool moLinearAlgebraReductionTool;
    moLinearAlgebraReductionTool.INoCoords(Degree);
    //////////////////// HERE /////////////////////////////////////////
    while (SomeLinearAlgebraToDo) {

        moLinearAlgebraReductionTool.INoPoints(weights.size());
        //moLinearAlgebraReductionTool.INoPoints((integer)bhBufInfo.iNoTrees);
        moLinearAlgebraReductionTool.MoveMass(weights, points, maxset);

        if (maxset.empty()) SomeLinearAlgebraToDo = false;
        while (maxset.size()) {
            index_integer togoposition(maxset.back());
            maxset.pop_back();
            miTreePosition.erase(currentroots[togoposition]);
            currentroots.erase(togoposition);
            // if there is at least one non-trivial tree split the last
            // (and so deepest) one to fill vacant slot
            index_integer tosplit(miTreePosition.rbegin()->first);
            if (!bhBufInfo.isleaf(tosplit)) {
                index_integer tosplitposition = miTreePosition[tosplit];
                miTreePosition.erase(tosplit);
                currentroots.erase(tosplitposition);

                currentroots[togoposition] = bhBufInfo.left(tosplit);
                miTreePosition[bhBufInfo.left(tosplit)] = togoposition;
                weights[togoposition] =
                        weights[tosplitposition] * vdWeightsBuffer[bhBufInfo.left(tosplit)] / vdWeightsBuffer[tosplit];

                currentroots[tosplitposition] = bhBufInfo.right(tosplit);
                miTreePosition[bhBufInfo.right(tosplit)] = tosplitposition;
                weights[tosplitposition] *= vdWeightsBuffer[bhBufInfo.right(tosplit)] / vdWeightsBuffer[tosplit];

                for (index_integer iM = 0; iM < Degree; iM++) {
                    points[togoposition * Degree + iM] = (vdPointsBuffer[bhBufInfo.left(tosplit)])[iM];
                    points[tosplitposition * Degree + iM] = (vdPointsBuffer[bhBufInfo.right(tosplit)])[iM];
                }
            }
        }

        RepackPointBuffer(currentroots, miTreePosition, weights, points, Degree);
        ICountCalls = moLinearAlgebraReductionTool.INoCallsLinAlg();
        //SHOW(ICountCalls);
    }

    return ICountCalls;
}

index_integer InsertLeafData(sRecombineInterface& data, std::valarray<doublereal>& vdArrayPointsBuffer,
                             VECTORD& vdWeightsBuffer)
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

}// namespace recombine04
