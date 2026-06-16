add_executable(basic_read basic_read.c)
target_link_libraries(basic_read PRIVATE adxl355)
target_include_directories(basic_read PRIVATE ${CMAKE_SOURCE_DIR}/include)

add_executable(configure_range configure_range.c)
target_link_libraries(configure_range PRIVATE adxl355)
target_include_directories(configure_range PRIVATE ${CMAKE_SOURCE_DIR}/include)

add_executable(mock_demo mock_demo.c ${CMAKE_SOURCE_DIR}/tests/test_mock_bus.c)
target_link_libraries(mock_demo PRIVATE adxl355)
target_include_directories(mock_demo PRIVATE ${CMAKE_SOURCE_DIR}/include ${CMAKE_SOURCE_DIR}/tests)
