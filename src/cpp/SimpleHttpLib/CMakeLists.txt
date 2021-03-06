cmake_minimum_required(VERSION 2.6)
cmake_policy(VERSION 2.6)

project(SimpleHttpLib)

if (NOT DEFINED ENV{DNANEXUS_HOME})
  message (FATAL_ERROR "Environment variable DNANEXUS_HOME (location of dx-toolkit) not defined")
endif (NOT DEFINED ENV{DNANEXUS_HOME})

# Set default build type, common compiler flags, etc
include("$ENV{DNANEXUS_HOME}/src/cpp/cmake_include/set_compiler_flags.txt" NO_POLICY_SCOPE)

#########################
# Find Boost header files
#########################
# Note: SimpleHttpHeaders.cpp just needs a Boost header files (no libraries are required)
#       Therefore, we just add boost include directory to include path
find_package(Boost 1.48 REQUIRED)
include_directories(BEFORE ${Boost_INCLUDE_DIR})
message (STATUS "SimpleHttpLib CMakeLists.txt says: Boost 1.48+ header files found in location ${Boost_INCLUDE_DIR}")
###################################

# Get the output of command `git describe`, and save it in DXTOOLKIT_GITVERSION variable
execute_process(COMMAND git describe WORKING_DIRECTORY $ENV{DNANEXUS_HOME} RESULT_VARIABLE GIT_DESCRIBE_STATUS_CODE OUTPUT_VARIABLE DXTOOLKIT_GITVERSION ERROR_VARIABLE GIT_DESCRIBE_ERROR)
if (GIT_DESCRIBE_STATUS_CODE EQUAL 0)
  # Trim the newline at the end of "git describe" output
  string(REGEX REPLACE "\n" "" DXTOOLKIT_GITVERSION ${DXTOOLKIT_GITVERSION})
  message(STATUS "SimpleHttpLib CMakeLists.txt says: DXTOOLKIT_GITVERSION= ${DXTOOLKIT_GITVERSION}")
else()
  set(DXTOOLKIT_GITVERSION unknown)
  message(STATUS "SimpleHttpLib CMakeLists.txt says: The command 'git describe' failed.")
  message(STATUS "\terror message: '${GIT_DESCRIBE_ERROR}'. Will set DXTOOLKIT_GITVERSION='${DXTOOLKIT_GITVERSION}'")
endif()
add_definitions(-DDXTOOLKIT_GITVERSION=\"${DXTOOLKIT_GITVERSION}\")

########################################
# Find libcurl include path/library path
########################################
find_path(CURL_INCLUDE_DIR curl/curl.h HINTS "/usr/include")
find_library(CURL_LIBRARY_PATH NAMES curl libcurl HINTS "/usr/lib")

if (CURL_INCLUDE_DIR AND CURL_LIBRARY_PATH)
  message(STATUS "SimpleHttpLib CMakeLists.txt says: libcurl found!")
  message(STATUS "\t** CURL_INCLUDE_PATH = \"${CURL_INCLUDE_DIR}\"")
  message(STATUS "\t** CURL_LIBRARY_PATH = \"${CURL_LIBRARY_PATH}\"")
else()
  message(FATAL_ERROR "\nSimpleHttpLib says: Unable to find libcurl. CURL_INCLUDE_PATH = \"${CURL_INCLUDE_DIR}\", CURL_LIBRARY_PATH = \"${CURL_LIBRARY_PATH}\"")
endif()
include_directories(BEFORE ${CURL_INCLUDE_DIR})
########################################

#######################################
# Find libcrypto (and openssl/crypto.h)
#######################################
find_path(OPENSSL_INCLUDE_DIR openssl/crypto.h)
find_library(CRYPTO_LIBRARY_PATH NAMES crypto)

if (OPENSSL_INCLUDE_DIR AND CRYPTO_LIBRARY_PATH)
  message(STATUS "SimpleHttpLib CMakeLists.txt says: libcrypto, and openssl/crypto.h found!")
  message(STATUS "\t** OPENSSL_INCLUDE_PATH = \"${OPENSSL_INCLUDE_DIR}\"")
  message(STATUS "\t** CRYPTO_LIBRARY_PATH = \"${CRYPTO_LIBRARY_PATH}\"")
else()
  message(FATAL_ERROR "\ndxcpp says: Unable to find 'libcrypto', and/or 'openssl/crypto.h'. OPENSSL_INCLUDE_PATH = \"${OPENSSL_INCLUDE_DIR}\", CRYPTO_LIBRARY_PATH = \"${CRYPTO_LIBRARY_PATH}\"")
endif()
include_directories(BEFORE ${OPENSSL_INCLUDE_DIR})
######################################

add_library(dxhttp SimpleHttp.cpp Utility.cpp SimpleHttpHeaders.cpp SSLThreads.cpp)
target_link_libraries (dxhttp ${CURL_LIBRARY_PATH} ${CRYPTO_LIBRARY_PATH})
