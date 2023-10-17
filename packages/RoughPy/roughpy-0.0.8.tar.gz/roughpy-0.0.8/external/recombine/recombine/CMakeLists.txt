cmake_minimum_required(VERSION 3.21)



include(GenerateExportHeader)


add_library(recombine SHARED )
add_library(recombine::recombine ALIAS recombine)


generate_export_header(recombine)

set(RECOMBINE_DEPENDENT_LIBS)

#if (RECOMBINE_ARCH STREQUAL x86_64)
#    set(BLA_SIZEOF_INTEGER ${RECOMBINE_BLA_INT_SIZE})
#endif ()

set(RECOMBINE_DEPENDENT_LIBS)


if (MSVC)
    target_compile_options(recombine PRIVATE /fp:precise)
endif()


# Set up blas/lapack

if(EXISTS ENV{MKLROOT} AND NOT "$ENV{MKLROOT}")
    message(FATAL_ERROR "MKLROOT set incorrectly")
endif()

if (CMAKE_SYSTEM_PROCESSOR MATCHES "arm" OR (APPLE AND CMAKE_OSX_ARCHITECTURES MATCHES arm64))
    set(_no_mkl ON)
else()
    set(_no_mkl OFF)
endif()

if (WIN32)
    set(_bla_static OFF)
    set(_bla_sizeof_int 4)
    if (NOT _no_mkl)
        set(MKL_THREADING intel_threads)
        set(MKL_LINK static)
        set(MKL_INTERFACE ilp64)
        find_package(MKL CONFIG QUIET)
    endif()
elseif(APPLE)
    set(_bla_static ON)
    set(_bla_vendor Apple)
    set(_bla_sizeof_int 4) # Accelerate doesn't support 64-bit indexing
    if (NOT _no_mkl)
        # On Intel Mac, MKL is our best best, try to find that
        find_package(MKL CONFIG QUIET)
    endif()
else()
    set(_bla_sizeof_int 4)
    set(_bla_static ON)

    if (NOT _no_mkl)
        set(MKL_THREADING intel_threads)
        set(MKL_LINK static)
        set(MKL_INTERFACE ilp64)
        find_package(MKL CONFIG QUIET)
    endif()
endif()

if(NOT TARGET MKL::MKL)
    if (NOT DEFINED BLA_VENDOR)
        set(BLA_VENDOR ${_bla_vendor})
    endif()
    if (NOT DEFINED BLA_STATIC)
        set(BLA_STATIC ${_bla_static})
    endif()
    if (NOT DEFINED BLA_SIZEOF_INTEGER)
        set(BLA_SIZEOF_INTEGER ${_bla_sizeof_int})
    endif()
    find_package(BLAS REQUIRED)
    find_package(LAPACK REQUIRED)
    target_link_libraries(recombine PRIVATE BLAS::BLAS LAPACK::LAPACK)
else()
    target_link_libraries(recombine PRIVATE MKL::MKL)
endif()

unset(_bla_vendor)
unset(_bla_static)
unset(_bla_sizeof_int)

#set(BLA_STATIC ON)
#set(MKL_LINK static)
#if (WIN32 OR MSVC)
#
#    if (RECOMBINE_ARCH STREQUAL x86_64)
#        if (RECOMBINE_USE_MKL)
#            if (RECOMBINE_BLA_INT_SIZE STREQUAL 4)
#                set(BLA_VENDOR Intel10_64lp)
#                set(MKL_INTERFACE lp64)
#            else()
#                set(BLA_VENDOR Intel10_64ilp)
#                set(MKL_INTERFACE ilp64)
#            endif()
#        endif ()
#        set(MKL_ARCH intel64)
#    elseif(RECOMBINE_ARCH STREQUAL x86)
#        if (RECOMBINE_USE_MKL)
#            set(BLA_VENDOR Intel10_32)
#        endif()
#        set(MKL_ARCH ia32)
#    endif()
#elseif (APPLE)
#    if (RECOMBINE_ARCH STREQUAL x86_64)
#        set(BLA_VENDOR Intel10_64ilp)
#        set(MKL_ARCH intel64)
#        set(MKL_INTERFACE ilp64)
#    else()
#        set(BLA_VENDOR generic)
#    endif()
#else()
#    if (RECOMBINE_ARCH STREQUAL x86_64)
#        set(BLA_VENDOR Intel10_64ilp)
#        set(MKL_ARCH intel64)
#        set(MKL_INTERFACE ilp64)
#    else ()
#        set(BLA_VENDOR Intel10_32)
#        set(MKL_ARCH ia32)
#        target_compile_options(recombine PRIVATE -m32)
#    endif ()
#endif ()


message(DEBUG "BLA_VENDOR: ${BLA_VENDOR}")
message(DEBUG "BLA_STATIC: ${BLA_STATIC}")
message(DEBUG "BLA_SIZEOF_INTEGER: ${BLA_SIZEOF_INTEGER}")
find_package(Threads REQUIRED)
find_package(OpenMP REQUIRED COMPONENTS CXX)

#if (NOT )
#    set(OpenMP_pthread_LIBRARY -lpthread)
#    find_package(OpenMP REQUIRED)
#endif()



#set(MKL_THREADING intel_thread)
#find_package(MKL CONFIG)
#if (MKL_FOUND)
#    message(STATUS "Using MKL")
#    target_link_libraries(recombine PRIVATE MKL::MKL)
#    message(STATUS "OMP library: ${OMP_LIBRARY}")
#    #list(APPEND RECOMBINE_DEPENDENT_LIBS "${OMP_LIBRARY}")
#    target_compile_definitions(recombine PRIVATE MKL)
#    message(STATUS "MKL_OMP_DLL ${OMP_DLLNAME}")
#    if (WIN32)
#        list(APPEND RECOMBINE_DEPENDENT_LIBS "${OMP_DLL_DIR}/${OMP_DLLNAME}")
#    else()
#        list(APPEND RECOMBINE_DEPENDENT_LIBS "${OMP_LIBRARY}")
#    endif()
#else()
#    unset(BLA_VENDOR)
##    set(BLA_VENDOR ATLAS)
#    set(BLA_VENDOR Apple)
#    set(BLA_SIZEOF_INTEGER 4)
#    set(CMAKE_REQUIRED_FLAGS "-lm")
#
#
#    message(STATUS  "BLA_VENDOR ${BLA_VENDOR}")
#    find_package(LAPACK REQUIRED)
#    if ("${LAPACK_LIBRARIES}" MATCHES mkl)
#        target_compile_definitions(recombine PRIVATE MKL)
#    endif()
#    # LAPACK sometimes needs the Fortran runtime library, so we add these to the interface
#    # so they are correctly linked to the target.
#    target_link_libraries(LAPACK::LAPACK INTERFACE ${CMAKE_Fortran_IMPLICIT_LINK_LIBRARIES})
#    target_link_libraries(recombine PRIVATE LAPACK::LAPACK)
#    unset(CMAKE_REQUIRED_FLAGS)
#endif()



#set(OpenMP_pthread_LIBRARY -lpthread)


if(MSVC)
    set(OpenMP_CXX_FLAGS -openmp:experimental)
    set_target_properties(OpenMP::OpenMP_CXX PROPERTIES INTERFACE_COMPILE_OPTIONS "-openmp:experimental")
endif()
message(STATUS "OpenMP_CXX_FLAGS: ${OpenMP_CXX_FLAGS}")
message(STATUS "OpenMP_CXX_INCLUDE_DIRS: ${OpenMP_CXX_INCLUDE_DIRS}")
message(STATUS "OpenMP_CXX_LIB_NAMES: ${OpenMP_CXX_LIB_NAMES}")
message(STATUS "OpenMP_CXX_LIBRARIES: ${OpenMP_CXX_LIBRARIES}")

target_link_libraries(recombine PRIVATE OpenMP::OpenMP_CXX)

target_sources(recombine PRIVATE
    recombine/Compare.cpp
    recombine/recombine.cpp
    recombine/LinearAlgebraReductionTool.cpp
    recombine/LinearAlgebraReductionTool.h
    recombine/reweight.h
    recombine/TreeBufferHelper.h
    recombine/TreeBufferHelper.cpp
    recombine/RdToPowers.h
    recombine/RdToPowers.cpp
)

set(INTF_HDRS
	recombine/recombine.h
	recombine/BufferConstructor.h
)

set_target_properties(recombine PROPERTIES
        PUBLIC_HEADER "${INTF_HDRS}"
        VERSION ${PROJECT_VERSION}
        SOVERSION ${PROJECT_VERSION_MAJOR}
        )
if(APPLE AND RECOMBINE_MAKE_FRAMEWORK)
    message(STATUS "Creating Apple Framework")
    set_target_properties(recombine PROPERTIES
      FRAMEWORK TRUE
      FRAMEWORK_VERSION C
      MACOSX_FRAMEWORK_IDENTIFIER com.cmake.recombine
      XCODE_ATTRIBUTE_CODE_SIGN_IDENTITY "Terry Lyons"
    )
endif()

if(RECOMBINE_NO_SONAME)
    set_target_properties(recombine PROPERTIES NO_SONAME ON)
endif()

target_include_directories(recombine PRIVATE
	recombine
	TestBlas
        PUBLIC
        "$<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>"
        "$<BUILD_INTERFACE:${CMAKE_CURRENT_LIST_DIR}>"
        "$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>"
)


target_compile_definitions(recombine
	PRIVATE
	NOSIMPLEX
	REDUCTION_ALGO=svd
	RECOMBINE_EXPORTS
	NDEBUG
)


configure_file(recombine.pc.in ${CMAKE_BINARY_DIR}/recombine.pc @ONLY)

include(GNUInstallDirs)

install(
	TARGETS recombine
	EXPORT recombine
   FRAMEWORK DESTINATION "${CMAKE_INSTALL_PREFIX}"
   # https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPFrameworks/Tasks/InstallingFrameworks.html
	RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}"
	ARCHIVE DESTINATION "${CMAKE_INSTALL_LIBDIR}"
	LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}"
	INCLUDES DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}" # where to look
	PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/recombine # where to put them
)

set(INSTALL_LAPACK_LIBRARIES "${LAPACK_LIBRARIES}")
list(FILTER INSTALL_LAPACK_LIBRARIES EXCLUDE REGEX "-l[a-zA-Z0-9_]+")
message(STATUS "LAPACK install libraries ${INSTALL_LAPACK_LIBRARIES}")

#install(FILES ${INSTALL_LAPACK_LIBRARIES} DESTINATION ${CMAKE_INSTALL_LIBDIR})

install(
	EXPORT recombine
	FILE "recombine-config.cmake"
	NAMESPACE recombine::
	DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/recombine
)
install(
	FILES ${CMAKE_BINARY_DIR}/recombine.pc
	DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/pkgconfig
)
install(
        FILES "${CMAKE_CURRENT_BINARY_DIR}/recombine_export.h"
        DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}/recombine"
)


if (RECOMBINE_INSTALL_DEPENDENTS AND RECOMBINE_DEPENDENT_LIBS)
    if (WIN32)
        message(STATUS "Dependent libs ${RECOMBINE_DEPENDENT_LIBS}")
        install(FILES ${RECOMBINE_DEPENDENT_LIBS} DESTINATION ${CMAKE_INSTALL_BINDIR})
    else()
        install(FILES ${RECOMBINE_DEPENDENT_LIBS} DESTINATION ${CMAKE_INSTALL_LIBDIR})
    endif()
#    install(TARGETS recombine RUNTIME_DEPENDENCY_SET RECOMBINE_RUNTIME_DEPENDENTS)
#    install(RUNTIME_DEPENDENCY_SET RECOMBINE_RUNTIME_DEPENDENTS
#            PRE_INCLUDE_REGEXES "iomp5")
endif()
