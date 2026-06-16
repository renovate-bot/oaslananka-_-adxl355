/**
 * basic_read.c
 *
 * Minimal example showing how to use the ADXL355 driver.
 * This example uses a mock transport — replace with real SPI/I2C for hardware.
 */

#include "adxl355/adxl355.h"
#include <stdio.h>

int main(void)
{
    adxl355_status_t status;

    /* -----------------------------------------------------------------------
     * In a real application you would provide actual bus callbacks here.
     * For this example we simply demonstrate the API calls.
     * ----------------------------------------------------------------------- */

    /* Placeholder bus – will fail, which is expected for this demo */
    adxl355_bus_t bus;
    bus.read     = NULL;
    bus.write    = NULL;
    bus.delay_ms = NULL;
    bus.ctx      = NULL;

    adxl355_t dev;
    status = adxl355_init(&dev, &bus);
    if (status != ADXL355_OK) {
        printf("Init failed: %s\n", adxl355_status_string(status));
        return 1;
    }

    printf("ADXL355 Driver v%s\n", ADXL355_VERSION_STRING);
    printf("Device initialised (mock).\n");
    printf("Provide real bus callbacks for hardware operation.\n");

    return 0;
}
