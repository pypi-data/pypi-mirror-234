

#include "recombine_export.h"

#ifndef recombine_h__
#define recombine_h__

/*
Example for declarations that work in wndows and linux
#if defined _WIN32 || defined __CYGWIN__
  #ifdef BUILDING_DLL
	#ifdef __GNUC__
	  #define DLL_PUBLIC __attribute__ ((dllexport))
	#else
	  #define DLL_PUBLIC __declspec(dllexport) // Note: actually gcc seems to also supports this syntax.
	#endif
  #else
	#ifdef __GNUC__
	  #define DLL_PUBLIC __attribute__ ((dllimport))
	#else
	  #define DLL_PUBLIC __declspec(dllimport) // Note: actually gcc seems to also supports this syntax.
	#endif
  #endif
  #define DLL_LOCAL
#else
  #if __GNUC__ >= 4
	#define DLL_PUBLIC __attribute__ ((visibility ("default")))
	#define DLL_LOCAL  __attribute__ ((visibility ("hidden")))
  #else
	#define DLL_PUBLIC
	#define DLL_LOCAL
  #endif
#endif

extern "C" DLL_PUBLIC void function(int a);
class DLL_PUBLIC SomeClass
{
   int c;
   DLL_LOCAL void privateMethod();  // Only for use within this DSO
public:
   Person(int _c) : c(_c) { }
   static void foo(int a);
};
*/

// define RECOMBINE_EXPORTS globally when building the library and not otherwise.
#ifdef _WIN32
#ifdef RECOMBINE_EXPORTS
#define RECOMBINE_API __declspec(dllexport)
#else
#define RECOMBINE_API __declspec(dllimport)
#endif
#else
#ifdef RECOMBINE_EXPORTS
#define RECOMBINE_API __attribute__((visibility("default")))
#else
#define RECOMBINE_API
#endif
#endif

#include "BufferConstructor.h"

/*
This header file defines the interface for programs seeking to do data reduction. 

The key input data are 
1) a set of N1 distinct points
	identified only by pointers to structures of type void
	and associated weights (positive doubles); 
2) d
3) a function that converts a point 
into a vector of d doubles and which will know what type to convert the void pointers to
it can deduce d from the size of the offered buffer

The key output data
1) a set of N2 <= d+1 distinct non-negative integers < N1, marking the points we retain and 
2) an equal number of revised weights so that the expectations of the marked points and new 
weights agree with the old expectation

We offer one interface
 a pure C interface
*/


#ifdef __cplusplus
extern "C" {
#endif
void RECOMBINE_EXPORT Recombine(void* recombine_interface);
double RECOMBINE_EXPORT Compare(void* recombine_interface);


enum prodsswitch {
    Prods2 = 1,
    Prods_test = 2,
    Prods_nonrecursive3 = 3,
    Prods_nonrecursive2 = 4,
    Prods_nonrecursive = 5,
    Prods_wei1 = 6,
    Prods_cheb = 7,
    Prods = 8
};
RECOMBINE_EXPORT
void RdToPowers(void* pIn, double* pOut, void* vpCBufferHelper);
// the structure pointed to be arg3 must have intial segment
//struct CConditionedBufferHelper
//{
//	size_t SmallestReducibleSetSize;
//	size_t NoPointsToBeprocessed;
//	void* pvCConditioning;
//};
// and the buffers ARG1 and ARG2 must have at least the dimensions specified above.

/// Get the number of commuting monomials of degree stCubatureDegree in stDimension
/// letters. This will be the number of points expected after recombination.
RECOMBINE_EXPORT
size_t RdToPowersCubatureDimension(size_t stDimension, size_t stCubatureDegree);



// an example of a conditioning that might be used in a given callback function
struct CMultiDimensionalBufferHelper {
    // all commutative monomials of degree <= D in L letters
    size_t L;
    size_t D;
};

// the current interface uses
struct sCloud;
struct sRCloudInfo;
struct sRecombineInterface {
    sCloud* pInCloud;
    sRCloudInfo* pOutCloudInfo;
    size_t degree;
    expander fn;
    void* end;
};
// where end must be null
// a C structure that points to the locations and weights in the cloud
struct sCloud {
    size_t NoActiveWeightsLocations;
    double* WeightBuf;
    void* LocationBuf;
    void* end;
};

// a C structure for the returned information used for modifying the cloud
struct sRCloudInfo {
    size_t No_KeptLocations;// number actually returned
    double* NewWeightBuf;      // a buffer containing the weights of the kept Locations // capacity must be at least degree + 1
    size_t* KeptLocations;  // a buffer containing the offsets of the kept Locations // capacity must be at least degree + 1
    void* end;
};
// and in each case end must be null;
//

#ifdef __cplusplus
}// extern "C"
#endif
#endif// recombine_h__
