/**
 * mock_demo.c
 *
 * Full mock demonstration: probe, set range, read acceleration.
 * No hardware required.
 */

#include "adxl355/adxl355.h"
#include "../tests/test_mock_bus.h"
#include <stdio.h>

int main(void)
{
    adxl355_mock_bus_t mock;
    adxl355_mock_bus_init(&mock);
    adxl355_mock_bus_set_identity_ok(&mock);

    /* Set some fake acceleration values */
    adxl355_mock_bus_set_xyz_raw(&mock, 1000, -2000, 32000);

    adxl355_bus_t bus = adxl355_mock_bus_get_interface(&mock);
    adxl355_t dev;

    adxl355_status_t status;

    status = adxl355_init(&dev, &bus);
    if (status != ADXL355_OK) { printf("Init error\n"); return 1; }

    status = adxl355_probe(&dev);
    if (status != ADXL355_OK) { printf("Probe failed\n"); return 1; }

    adxl355_set_range(&dev, ADXL355_RANGE_2G);
    adxl355_set_power_mode(&dev, ADXL355_POWER_MEASUREMENT);

    /* Read raw */
    adxl355_raw_xyz_t raw;
    adxl355_read_raw(&dev, &raw);
    printf("Raw: x=%d, y=%d, z=%d\n", raw.x, raw.y, raw.z);

    /* Read in g */
    adxl355_float_xyz_t accel;
    adxl355_read_g(&dev, &accel);
    printf("Accel (g): x=%.6f, y=%.6f, z=%.6f\n", accel.x, accel.y, accel.z);

    /* Read in m/s² */
    adxl355_read_mps2(&dev, &accel);
    printf("Accel (m/s²): x=%.4f, y=%.4f, z=%.4f\n", accel.x, accel.y, accel.z);

    return 0;
}
