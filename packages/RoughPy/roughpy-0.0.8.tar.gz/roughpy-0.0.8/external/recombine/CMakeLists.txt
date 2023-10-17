# CMakeList.txt : Top-level CMake project file, do global configuration
# and include sub-projects here.
#
cmake_minimum_required (VERSION 3.21)

project(Recombine
        VERSION 2.0.2
        DESCRIPTION "Performs a dynamic Caratheodory process and takes a weighted collection of vectors and identifies by pointers, a subset of minimal cardinality among the vectors and new weights so both empirical measures have the same mean. Software written by Terry Lyons, based on algorithms developed jointly with Christian Litter and then with Maria Tchernychova 2008-2020. Any compiled library built by this cmake script may be used freely without any guarantee or liability. Otherwise, all rights reserved. For further information contact Terry Lyons, software@lyonstech.net"
        )

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_CXX_VISIBILITY_PRESET hidden)
set(CMAKE_VISIBILITY_INLINES_HIDDEN ON)


option(TEST_RECOMBINE "Enable building recombine test suite" ON)
option(RECOMBINE_USE_MKL "Use MKL BLAS library" ON)
option(RECOMBINE_MAKE_FRAMEWORK "Make an framework on Apple" ON)
option(RECOMBINE_INSTALL_DEPENDENTS "Install dependency runtimes alongside" OFF)
option(RECOMBINE_NO_SONAME "Do not add SO NAME to library files" OFF)

cmake_host_system_information(RESULT RECOMBINE_64BIT QUERY IS_64BIT)
if (NOT DEFINED RECOMBINE_ARCH)
    # TODO: Handle ARM
    if (CMAKE_SIZEOF_VOID_P STREQUAL 8)
        set(RECOMBINE_ARCH "x86_64")
    else()
        set(RECOMBINE_ARCH "x86")
    endif()
endif ()
message(STATUS "Recombine arch ${RECOMBINE_ARCH}")
if (NOT DEFINED RECOMBINE_BLA_INT_SIZE)
    set(RECOMBINE_BLA_INT_SIZE "${CMAKE_SIZEOF_VOID_P}")
endif()



if ("${CMAKE_SOURCE_DIR}" EQUAL "${CMAKE_CURRENT_SOURCE_DIR}")
    set(RECOMBINE_IS_SUBPROJECT ON)
else()
    set(RECOMBINE_IS_SUBPROJECT OFF)
endif()



##set (CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
include(GNUInstallDirs)

# Include sub-projects.
add_subdirectory(recombine)

if (TEST_RECOMBINE AND NOT RECOMBINE_IS_SUBPROJECT)
    add_subdirectory(test_recombine)
    set_property(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY VS_STARTUP_PROJECT test_recombine)
endif()
