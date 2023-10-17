#ifndef RdToPowers_h__
#define RdToPowers_h__

#include <cstddef>

#ifdef __cplusplus
extern "C"
{
#endif

typedef double SCA;
typedef SCA* PSCA;

void prods(PSCA& now, SCA val, size_t k, const size_t D, const SCA* ptv, const SCA* end);


#ifdef __cplusplus
}
#endif

#endif // RdToPowers_h__
