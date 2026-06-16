cmake_minimum_required(VERSION 3.14)
project(adxl355-cpp VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

option(ADXL355_BUILD_TESTS    "Build tests"    OFF)
option(ADXL355_BUILD_EXAMPLES "Build examples" OFF)

# The C++ wrapper links against the C core library
# Adjust path as needed
find_library(ADXL355_C_LIB adxl355 PATHS ${CMAKE_SOURCE_DIR}/../c/build)
if(NOT ADXL355_C_LIB)
    message(WARNING "C core library (adxl355) not found. "
                    "Build the C library first: cmake -S c -B c/build && cmake --build c/build")
endif()

add_library(adxl355_cpp INTERFACE)
target_include_directories(adxl355_cpp INTERFACE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_SOURCE_DIR}/../c/include
)
if(ADXL355_C_LIB)
    target_link_libraries(adxl355_cpp INTERFACE ${ADXL355_C_LIB})
endif()

# ---- Tests ------------------------------------------------------------------
if(ADXL355_BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()

# ---- Examples ---------------------------------------------------------------
if(ADXL355_BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()
