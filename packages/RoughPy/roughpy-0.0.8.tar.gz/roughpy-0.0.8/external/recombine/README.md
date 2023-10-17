![build-linux](https://github.com/terrylyons/recombine/workflows/build-linux/badge.svg)
![build-macOS](https://github.com/terrylyons/recombine/workflows/build-macOS/badge.svg)
![build-windows](https://github.com/terrylyons/recombine/workflows/build-windows/badge.svg)

# Recombine
A shared C++ library for dynamic caratheodory data simplification with a robust and stable C interface.

Performs a dynamic Caratheodory process and takes a weighted collection of vectors and identifies by pointers, a subset of minimal cardinality among the vectors and new weights so both empirical measures have the same mean. 
Software written by Terry Lyons, based on algorithms developed jointly with Christian Litter and then with Maria Tchernychova 2008-2020. 
Here minimal is a local notion and means it cannot be further reduced. 
There may be other noncomparable cubature sets with fewer points.

The library has a robust and stable C interface and even old dlls from 2008 with the old algorithm still run. 
Measures are represented by an array of null pointers (pseudo-points) and an array of equal length of positive doubles adding to `1.`; the calling program provides a feature map that converts each null pointer to a vector, and so recombine never knows or needs to know the real types of the points. 
Recombine returns the indexes of the points that should remain and new positive weights so that the mean of these remaining points with the new weights is the same as the old mean. 
The new list of survivors is never more than `D+1` long where `D` is the  dimension of the vector space. 
If there are `N` points in `D` dimensions the sequential complexity of this algorithm is less  than `ND + log_2(N/D) D^3`. 
This reflects the order of magnitude improvement in the algorithm developed with  Maria Tchernychova; the algorithm with Litterer had complexity `ND + log_2(N/D) D^4` although it is quicker for small problems. 
The interface remains the same. 
The ND comes from touching the points, and `log_2(N/D) D^3` from performing `log_2(N/D)` complex SVD type calculations on `Dx2D` matrices. 
This is a linear programming problem under the surface, but the algorithm here has fixed complexity. 
In many of the problems we are interested in `N` is approximately `D^2` so the cost is (to logarithms) equated with the cost of touching the points.

The algorithm uses MKL (LAPACK) to do most of the linear algebra, although there is a part that is bespoke. 
The operations benefit from some parallelism via OMP. 
Say (export OMP_NUM_THREADS=8). 
The log factor is truly sequential.


# Getting started
The library is accompanied by a test program that can easily be modified for your own purposes. 
It takes 10000 random vectors of dimension 100 and normal N(0,1) entries. 
It finds a minimal number (101 at most) of them with new weights and checks they have the same mean.
The output is the L1 norm of the difference of the means, normalised by the sum of the L1 norms of the means. 
Followed by confirmation of the number of points and the final number of points. 
This test returns 0 if the difference is less than 10^-11.

To repeat this yourself you should clone the repository, and build the binaries. 
The build information is easily setup for windows and unix. 
You will need a recent version of cmake installed. 
After setting up the prerequistes for your system associated with MKL and listed below, TODO.... 
However test-recombine cannot be built on its own until after recombine has been built.

## Setting up BLAS/LAPACK

### Intel MKL
If you install intel MKL and then run their script that sets/exports everything including $MKLROOT it should begin to work. 
You must set and export MKLROOT. 
The code also needs to find libiomp5md.so at runtime. 
To use it successfully in other code one needs to add $HOME/lyonstech/lib to the LD_LIBRARY_PATH variable and make sure the system can find the libiomp5md.so/dll by permanently adding the path to LD_LIBRARY_PATH In linux or adding the file to $HOME/lyonstech/lib In windows. 
If you edit the doall file the base prefix location can be changed but must be consistent across all components.
libiompmd5.[so|dll]: In Linux it needs to be in the LD_DIRECTORY_PATH and in Windows will need it to be in the folder with the exe lyonstech/bin or added to the path. 
In linux the so file is in $MKLROOT/lib/intel64/compiler and in windows the dll file is in  %MKLROOT%\..\redist\intel64\compiler


# License
This library is licensed under a BSD-3-Clause licence.
This licence was specifically chosen because it is also used by the Python numerical array library Numpy, which we view as having a similar use case.
