# CMakeList.txt : CMake project for test_recombine, include source and define
# project specific logic here.
#
cmake_minimum_required (VERSION 3.18)
set(CMAKE_CXX_STANDARD 11)
project(test_recombine VERSION 2.0.2 DESCRIPTION "simple tests for recombine")

# https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=223678
set(OpenMP_pthread_LIBRARY -lpthread)
find_package(OpenMP REQUIRED)

# Add source to this project's executable.
add_executable (test_recombine
test_recombine.cpp
test_recombine.h
#TestVec/EvaluateAllMonomials.h
#TestVec/OstreamContainerOverloads.h
        TestVec/ScopedWindowsPerformanceTimer.cpp
TestVec/ScopedWindowsPerformanceTimer.h
TestVec/stdafx.h
TestVec/targetver.h
lib/SHOW.h
#set_env_test_recombine.sh
)
if(TARGET recombine)
   # in the build tree
   target_link_libraries(test_recombine recombine #[[OpenMP::OpenMP_CXX]])
    target_include_directories(test_recombine PRIVATE ../recombine)
else(TARGET recombine)
   # use external library already installed
   find_package(recombine REQUIRED)
   target_link_libraries(test_recombine recombine::recombine #[[OpenMP::OpenMP_CXX]])
endif(TARGET recombine)

if(MSVC)
   set_target_properties(recombine PROPERTIES LINK_FLAGS /STACK:15000000)
endif()

set_target_properties(test_recombine PROPERTIES INSTALL_RPATH "@executable_path/..")

target_include_directories(test_recombine PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

add_custom_command(TARGET test_recombine POST_BUILD
                   COMMAND ${CMAKE_COMMAND} -E copy_if_different
                       ${CMAKE_CURRENT_SOURCE_DIR}/set_env_test_recombine.sh
                       $<TARGET_FILE_DIR:test_recombine>
                   )
