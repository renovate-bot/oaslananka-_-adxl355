cmake_minimum_required(VERSION 3.14)
project(adxl355 VERSION 0.1.0 LANGUAGES C)

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)

# ---- Options ---------------------------------------------------------------
option(ADXL355_BUILD_TESTS    "Build tests"    OFF)
option(ADXL355_BUILD_EXAMPLES "Build examples" OFF)
option(ADXL355_ENABLE_WARNINGS    "Enable compiler warnings"             ON)
option(ADXL355_WARNINGS_AS_ERRORS "Treat compiler warnings as errors"    OFF)

# ---- Public headers --------------------------------------------------------
set(ADXL355_PUBLIC_HEADERS
    include/adxl355/adxl355.h
    include/adxl355/adxl355_registers.h
    include/adxl355/adxl355_version.h
)

# ---- Library ---------------------------------------------------------------
add_library(adxl355
    src/adxl355.c
    ${ADXL355_PUBLIC_HEADERS}
)

target_include_directories(adxl355
    PUBLIC  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
            $<INSTALL_INTERFACE:include>
)

# ---- Warnings --------------------------------------------------------------
if(ADXL355_ENABLE_WARNINGS)
    if(CMAKE_C_COMPILER_ID MATCHES "GNU|Clang")
        target_compile_options(adxl355 PRIVATE
            -Wall -Wextra -Wpedantic
            -Wshadow -Wconversion -Wsign-conversion
            -Wimplicit-fallthrough -Wundef
        )
        if(ADXL355_WARNINGS_AS_ERRORS)
            target_compile_options(adxl355 PRIVATE -Werror)
        endif()
    elseif(MSVC)
        target_compile_options(adxl355 PRIVATE /W4)
        if(ADXL355_WARNINGS_AS_ERRORS)
            target_compile_options(adxl355 PRIVATE /WX)
        endif()
    endif()
endif()

# ---- Tests -----------------------------------------------------------------
if(ADXL355_BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()

# ---- Examples --------------------------------------------------------------
if(ADXL355_BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()

# ---- Install ---------------------------------------------------------------
include(GNUInstallDirs)
install(TARGETS adxl355 EXPORT adxl355-targets
    ARCHIVE  DESTINATION ${CMAKE_INSTALL_LIBDIR}
    LIBRARY  DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME  DESTINATION ${CMAKE_INSTALL_BINDIR}
)
install(FILES ${ADXL355_PUBLIC_HEADERS}
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/adxl355
)
install(EXPORT adxl355-targets
    NAMESPACE adxl355::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/adxl355
)
