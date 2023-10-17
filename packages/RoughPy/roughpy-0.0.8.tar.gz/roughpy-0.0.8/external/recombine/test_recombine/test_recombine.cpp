// test_recombine.cpp : Defines the entry point for the application.
//

#include "test_recombine.h"
#include "TestVec/EvaluateAllMonomials.h"         //EvaluateAllMonomials::F
#include "TestVec/ScopedWindowsPerformanceTimer.h"//CScopedWindowsPerformanceTimer
#include "lib/SHOW.h"
#include <random>
#include <recombine/recombine.h>
#include <valarray>

//using namespace std;

// https://stackoverflow.com/questions/14446495/cmake-project-structure-with-unit-tests
//

std::default_random_engine generator;
std::normal_distribution<> distribution(0, 1);

class RandomMatrix {
	std::valarray<double> data;
	size_t dim;
public:
	RandomMatrix(size_t r, size_t c) : data(r* c), dim(c) {
		for (auto i = begin(data); i != end(data); ++i)
			*i = distribution(generator);
	}

	double& operator()(size_t r, size_t c) { return data[r * dim + c]; }
	auto row(size_t r)->std::valarray<double> const { return data[std::slice(r * dim, dim, 1)]; }
	auto column(size_t c)->std::valarray<double> const { return data[std::slice(c, (end(data) - begin(data)) / dim, dim)]; }
	double trace() const { return data[std::slice(0, dim, dim + 1)].sum(); }
};

std::valarray<double> get_mean(size_t dimension, ptrdiff_t no_points, RandomMatrix& A)
{
	std::valarray<double> mean(dimension);
	for (ptrdiff_t i = 0; i < no_points; ++i)
		mean += A.row(i);
	mean /= double(no_points);
	return mean;
}

std::valarray<double> get_indexed_mean(size_t dimension, size_t no_points, RandomMatrix& A
	, const std::vector<size_t>& indices
	, const std::vector<double>& weights
)
{
	std::valarray<double> mean(dimension);
	for (ptrdiff_t i = 0; i < end(indices) - begin(indices); ++i)
		mean += weights[i] * A.row(indices[i]);
	return mean;
}

size_t compare(const std::valarray<double>& mean1, const std::valarray<double>& mean2)
{
	double err = (abs(mean1 - mean2)).sum() / ((abs(mean1)).sum() + (abs(mean2)).sum());
	return (err < 1e-12);
}

int main()
{
	ptrdiff_t no_points = 10000;
	ptrdiff_t dimension = 100;

// create the data
	RandomMatrix A(no_points, dimension);
	std::vector<double> weights(no_points, 1. / double(no_points));
// index the array
	std::vector<size_t> indices(no_points);
	for (ptrdiff_t i = 0; i < no_points; ++i)
		indices[i] = i;
// utilize existing code for moments but only use degree 1; hgher degrees should also work!
size_t stCubatureDegree = 1;

// set up data for the recombine process
	// create the input buffer of void pointers capturing the locations of points
	std::vector<const void*> vpLocationBuffer(no_points);
	// create the input buffer of double pointers capturing the weights of points
	std::vector<double> vdWeightBuffer(no_points);
// populate the buffers
	for (ptrdiff_t i = 0; i < no_points; ++i)
	{
		vpLocationBuffer[i] = &A(i,0);
		vdWeightBuffer[i] = weights[i];
	}

// set up the input structure for conditioning the helper function
	CMultiDimensionalBufferHelper sConditioning;
	sConditioning.D = stCubatureDegree;
	sConditioning.L = dimension;

	// set up the input structure for data reduction "in"
	sCloud in;

	// chain optional extension information used to condition the data
	in.end = &sConditioning;

	// place the sizes of the buffers and their locations into the structure "in"
	in.NoActiveWeightsLocations = no_points;
	in.LocationBuf = &vpLocationBuffer[0];
	in.WeightBuf = &vdWeightBuffer[0];

	// set up the output structure for data reduction "out"
	sRCloudInfo out;
	out.end = 0;

	size_t iNoDimensionsToCubature = EvaluateAllMonomials::F(dimension, stCubatureDegree);

	// setup a buffer of size iNoDimensionsToCubature to store indexes to the kept points
	std::vector<size_t> KeptLocations(iNoDimensionsToCubature);

	// setup a buffer of size iNoDimensionsToCubature to store the weights of the kept points
	std::vector<double> NewWeights(iNoDimensionsToCubature);

	// set the locations of these buffers into the structure "out"
	out.KeptLocations = &KeptLocations[0];
	out.NewWeightBuf = &NewWeights[0];

	// and the max dimension of the buffers
	out.No_KeptLocations = iNoDimensionsToCubature;

	// setup the Recombine Interface data which will join the input and output
	sRecombineInterface data;
	data.end = 0;

	// bind in and out together in data
	data.pInCloud = &in;
	data.pOutCloudInfo = &out;

	// add the degree of the vectors used and the callback function that expands 
	// the array of pointers to points into a long buffer of vectors
	data.degree = iNoDimensionsToCubature;

	data.fn = &RdToPowers;

	double timer(0);
	{
		CScopedWindowsPerformanceTimer t1(timer);
// CALL THE LIBRARY THAT DOES THE HEAVYLIFTING
		Recombine(&data);
	}
// recover the information and resize buffers down to the data
	auto& No_KeptLocations(data.pOutCloudInfo->No_KeptLocations);
	NewWeights.resize(No_KeptLocations);
	KeptLocations.resize(No_KeptLocations);

	// Compute the means
	//auto mean1 = get_mean(dimension, no_points, A);
	auto mean2 = get_indexed_mean(
		dimension
		, no_points
		, A
		, indices
		, weights
	);
	auto mean3 = get_indexed_mean(
		dimension
		, no_points
		, A
		, KeptLocations
		, NewWeights
	);
	//std::cout << "The original mean is "; for (auto i : mean2) std::cout << i << ", "; std::cout << std::endl;
	//std::cout << "The index mean is "; for (auto i : mean3) std::cout << i << ", "; std::cout << std::endl;
	std::cout << (abs(mean2 - mean3)).sum() / ((abs(mean3)).sum() + (abs(mean2)).sum()) << " " << (abs(mean3)).sum() << " " << (abs(mean2)).sum() << std::endl;
	SHOW(no_points);
	SHOW(No_KeptLocations);
	SHOW(timer);
	std::cout << "returning:" << !compare(mean3, mean2) << std::endl;
	return !compare(mean3, mean2);
}
