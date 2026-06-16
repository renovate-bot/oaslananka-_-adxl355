add_executable(basic_read basic_read.c)
target_link_libraries(basic_read PRIVATE adxl355)
target_include_directories(basic_read PRIVATE ${CMAKE_SOURCE_DIR}/include)

add_executable(configure_range configure_range.c)
target_link_libraries(configure_range PRIVATE adxl355)
target_include_directories(configure_range PRIVATE ${CMAKE_SOURCE_DIR}/include)

add_executable(mock_demo mock_demo.c ${CMAKE_SOURCE_DIR}/tests/test_mock_bus.c)
target_link_libraries(mock_demo PRIVATE adxl355)
target_include_directories(mock_demo PRIVATE ${CMAKE_SOURCE_DIR}/include ${CMAKE_SOURCE_DIR}/tests)

# ── Linux hardware example (spidev) ──────────────────────────────────────
# Linux-only; depends on <linux/spi/spidev.h> and <sys/ioctl.h>
if(CMAKE_SYSTEM_NAME STREQUAL "Linux")
    add_executable(linux_spi linux_spi.c)
    target_link_libraries(linux_spi PRIVATE adxl355)
    target_include_directories(linux_spi PRIVATE ${CMAKE_SOURCE_DIR}/include)
    target_compile_definitions(linux_spi PRIVATE _GNU_SOURCE)
endif()
