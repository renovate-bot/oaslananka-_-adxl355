#include <adxl355/adxl355.hpp>
#include <cstdio>

int main() {
    std::printf("ADXL355 C++ Driver v%s\n", ADXL355_VERSION_STRING);

    // NOTE: This example requires a real bus implementation.
    // For a mock demo, see the test suite.
    std::printf("Provide a BusInterface implementation for hardware access.\n");

    return 0;
}
