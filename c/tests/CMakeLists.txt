add_executable(test_adxl355
    test_adxl355.c
    test_mock_bus.c
)

target_include_directories(test_adxl355 PRIVATE
    ${CMAKE_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}
)

target_link_libraries(test_adxl355 PRIVATE adxl355)

add_test(NAME test_adxl355 COMMAND test_adxl355)
