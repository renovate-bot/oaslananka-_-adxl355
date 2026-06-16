/**
 * configure_range.c
 *
 * Demonstrates range configuration with the ADXL355 driver.
 * NOTE: Requires real SPI/I2C hardware or a custom mock bus.
 *       Build with -DADXL355_BUILD_TESTS=ON and see mock_demo for mock demo.
 */

#include "adxl355/adxl355.h"
#include <stdio.h>

int main(void)
{
    printf("ADXL355 Range Configuration Example\n");
    printf("====================================\n");
    printf("\n");
    printf("This example requires a real SPI/I2C bus.\n");
    printf("For a mock demo:\n");
    printf("  cmake -S c -B c/build -DADXL355_BUILD_TESTS=ON -DADXL355_BUILD_EXAMPLES=ON\n");
    printf("  cmake --build c/build\n");
    printf("  ./c/build/examples/mock_demo\n");
    printf("\n");

    printf("API usage:\n");
    printf("  1. adxl355_init(&dev, &bus);\n");
    printf("  2. adxl355_probe(&dev);\n");
    printf("  3. adxl355_set_range(&dev, ADXL355_RANGE_8G);\n");
    printf("  4. adxl355_set_power_mode(&dev, ADXL355_POWER_MEASUREMENT);\n");
    printf("  5. adxl355_read_raw(&dev, &raw);\n");

    return 0;
}
