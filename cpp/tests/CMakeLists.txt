add_executable(test_adxl355_cpp test_adxl355_cpp.cpp)
target_link_libraries(test_adxl355_cpp PRIVATE adxl355_cpp)
target_include_directories(test_adxl355_cpp PRIVATE ${CMAKE_SOURCE_DIR}/include)

add_test(NAME test_adxl355_cpp COMMAND test_adxl355_cpp)
