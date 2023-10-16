def _cmake_to_bool(s):
    return s.upper() not in ['', '0','FALSE','OFF','N','NO','IGNORE','NOTFOUND']

is_python_package    = _cmake_to_bool("TRUE")

BUILD_STUB_FILES     = _cmake_to_bool("OFF")
BUILD_UMFPACK        = _cmake_to_bool("")
ENABLE_UNIT_TESTS    = _cmake_to_bool("OFF")
INSTALL_DEPENDENCIES = _cmake_to_bool("OFF")
USE_CCACHE           = _cmake_to_bool("ON")
USE_HYPRE            = _cmake_to_bool("OFF")
USE_LAPACK           = _cmake_to_bool("ON")
USE_MKL              = _cmake_to_bool("OFF")
USE_MKL              = _cmake_to_bool("OFF")
USE_MUMPS            = _cmake_to_bool("OFF")
USE_PARDISO          = _cmake_to_bool("OFF")
USE_UMFPACK          = _cmake_to_bool("ON")

NETGEN_DIR = "/Users/gitlab-runner/Library/Python/3.11/lib/python/site-packages"

NGSOLVE_COMPILE_DEFINITIONS         = "HAVE_NETGEN_SOURCES;HAVE_DLFCN_H;HAVE_CXA_DEMANGLE;USE_TIMEOFDAY;MSG_NOSIGNAL=0;TCL;LAPACK;NGS_PYTHON;USE_UMFPACK"
NGSOLVE_COMPILE_DEFINITIONS_PRIVATE = ""
NGSOLVE_COMPILE_INCLUDE_DIRS        = ""
NGSOLVE_COMPILE_OPTIONS             = "$<$<COMPILE_LANGUAGE:CXX>:-std=c++17>;$<$<COMPILE_LANGUAGE:CXX>:-Wno-undefined-var-template>;-DMAX_SYS_DIM=3"

NGSOLVE_VERSION = "6.2.2304-302-gf4a266510"
NGSOLVE_VERSION_GIT = "v6.2.2304-302-gf4a266510"
NGSOLVE_VERSION_PYTHON = "6.2.2304.post302.dev"

NGSOLVE_VERSION_MAJOR = "6"
NGSOLVE_VERSION_MINOR = "2"
NGSOLVE_VERSION_TWEAK = "302"
NGSOLVE_VERSION_PATCH = "2304"
NGSOLVE_VERSION_HASH = "gf4a266510"

CMAKE_CXX_COMPILER           = "/Library/Developer/CommandLineTools/usr/bin/c++"
CMAKE_CUDA_COMPILER          = ""
CMAKE_C_COMPILER             = "/Library/Developer/CommandLineTools/usr/bin/cc"
CMAKE_LINKER                 = "/Library/Developer/CommandLineTools/usr/bin/ld"
CMAKE_INSTALL_PREFIX         = "/Users/gitlab-runner/builds/builds/rL7WHzyj/0/ngsolve/ngsolve/_skbuild/macosx-10.15-universal2-3.11/cmake-install"
CMAKE_CXX_COMPILER_LAUNCHER  = "/usr/local/bin/ccache"

version = NGSOLVE_VERSION_GIT

def get_cmake_dir():
    import netgen.config as c
    import os.path as p
    d_python = p.dirname(p.dirname(__file__))
    py_to_cmake = p.relpath(
            p.dirname(c.NG_INSTALL_DIR_CMAKE),
            c.NG_INSTALL_DIR_PYTHON
            )
    return p.normpath(p.join(d_python,py_to_cmake, 'ngsolve'))
