add_executable(basic_read basic_read.cpp)
target_link_libraries(basic_read PRIVATE adxl355_cpp)
target_include_directories(basic_read PRIVATE ${CMAKE_SOURCE_DIR}/include)
