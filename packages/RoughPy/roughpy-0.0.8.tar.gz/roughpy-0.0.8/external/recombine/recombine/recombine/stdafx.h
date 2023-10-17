// stdafx.h : include file for standard system include files,
// or project specific include files that are used frequently, but
// are changed infrequently
//

#pragma once

#ifndef NOMINMAX
#define NOMINMAX
#endif
#define WIN32_LEAN_AND_MEAN// Exclude rarely-used stuff from Windows headers

//#include <tchar.h>
#include "lapack_defns.h"
#include <iostream>
#include <iterator>
#include <valarray>
#include <vector>

// TODO: reference additional headers your program requires here

template<class TT>
inline const TT& deref(const void* const arg)
{
    return *(const TT* const)arg;
}

template<class T, class TT>
class dereference {
    const T& container;

public:
    dereference(const T& arg)
        : container(arg){};

    friend std::ostream& operator<<(std::ostream& out, const dereference& arg)
    {
        out << '{';
        std::transform(arg.container.begin(), arg.container.end(), std::ostream_iterator<TT>(out, " "), deref<TT>);
        out << '}';
        return out;
    }
};

// TODO: reference additional headers your program requires here
