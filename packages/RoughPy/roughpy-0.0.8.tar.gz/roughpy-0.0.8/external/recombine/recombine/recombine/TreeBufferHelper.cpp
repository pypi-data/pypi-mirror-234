/* Copyright -  All Rights Reserved - Terry Lyons 2008 */

#include "TreeBufferHelper.h"

#include <cassert>//assert

CTreeBufferHelper::CTreeBufferHelper(index_integer SmallestReducibleSetSize, index_integer NoPointsToBeprocessed)
    : iNoTrees(SmallestReducibleSetSize),
      iInitialNoLeaves(NoPointsToBeprocessed)
{
    assert(iInitialNoLeaves >= iNoTrees && iNoTrees > 0);
}

bool CTreeBufferHelper::isleaf(const index_integer& node) const
{
    return (node < iInitialNoLeaves && node >= 0);
}

index_integer CTreeBufferHelper::end() const
{
    return 2 * iInitialNoLeaves - iNoTrees;
}

bool CTreeBufferHelper::isnode(const index_integer& node) const
{
    return node >= 0 && node < end();
}

index_integer CTreeBufferHelper::parent(const index_integer& node) const
{
    assert(isnode(node));
    return std::min(iInitialNoLeaves + (node / 2), end());
}

bool CTreeBufferHelper::isroot(const index_integer& node) const
{
    assert(isnode(node));
    return parent(node) == end();
}

index_integer CTreeBufferHelper::left(const index_integer& node) const
{
    assert(isnode(node));
    // returns negative if leaf
    return (node - iInitialNoLeaves) * 2;
}

index_integer CTreeBufferHelper::right(const index_integer& node) const
{
    return (left(node) < 0) ? -1 : left(node) + 1;
}
