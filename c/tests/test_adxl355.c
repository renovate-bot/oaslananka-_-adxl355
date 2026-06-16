#include "adxl355/adxl355.h"
#include "test_mock_bus.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

/* ---------------------------------------------------------------------------
 * Simple test framework (no external deps)
 * --------------------------------------------------------------------------- */
static int  g_tests_run  = 0;
static int  g_tests_pass = 0;
static int  g_tests_fail = 0;

#define TEST_ASSERT(cond, msg) do {                                     \
    g_tests_run++;                                                      \
    if (!(cond)) {                                                      \
        fprintf(stderr, "  FAIL [%s:%d] %s\n", __FILE__, __LINE__, msg);\
        g_tests_fail++;                                                 \
    } else {                                                            \
        g_tests_pass++;                                                 \
    }                                                                   \
} while(0)

#define TEST_START(name)   printf("\n--- %s ---\n", name)
#define TEST_END()         printf("  passed\n")

/* near-enough float comparison */
static int approx_eq(float a, float b, float eps)
{
    return fabsf(a - b) < eps;
}

/* ---------------------------------------------------------------------------
 * Tests
 * --------------------------------------------------------------------------- */

static void test_decode_raw20_zero(void)
{
    TEST_START("decode_raw20_zero");
    int32_t v = adxl355_decode_raw20(0, 0, 0);
    TEST_ASSERT(v == 0, "0,0,0 should decode to 0");
    TEST_END();
}

static void test_decode_raw20_positive_one(void)
{
    TEST_START("decode_raw20_positive_one");
    /* bytes: [0, 0, 16] => raw bit 0 set */
    int32_t v = adxl355_decode_raw20(0, 0, 16);
    TEST_ASSERT(v == 1, "should decode to 1");
    TEST_END();
}

static void test_decode_raw20_positive_max(void)
{
    TEST_START("decode_raw20_positive_max");
    int32_t v = adxl355_decode_raw20(127, 255, 240);
    TEST_ASSERT(v == 524287, "0x7FFFF = 524287");
    TEST_END();
}

static void test_decode_raw20_negative_min(void)
{
    TEST_START("decode_raw20_negative_min");
    int32_t v = adxl355_decode_raw20(128, 0, 0);
    TEST_ASSERT(v == -524288, "0x80000 = -524288");
    TEST_END();
}

static void test_decode_raw20_negative_one(void)
{
    TEST_START("decode_raw20_negative_one");
    int32_t v = adxl355_decode_raw20(255, 255, 240);
    TEST_ASSERT(v == -1, "0xFFFFF = -1");
    TEST_END();
}

static void test_raw_to_g_2g(void)
{
    TEST_START("raw_to_g_2g");
    float g = adxl355_raw_to_g(524287, ADXL355_RANGE_2G);
    float expected = 524287.0f * 0.0000039f;
    TEST_ASSERT(approx_eq(g, expected, 1e-6f), "raw 524287 @ 2g");
    TEST_END();
}

static void test_raw_to_g_4g(void)
{
    TEST_START("raw_to_g_4g");
    float g = adxl355_raw_to_g(524287, ADXL355_RANGE_4G);
    float expected = 524287.0f * 0.0000078f;
    TEST_ASSERT(approx_eq(g, expected, 1e-6f), "raw 524287 @ 4g");
    TEST_END();
}

static void test_raw_to_g_8g(void)
{
    TEST_START("raw_to_g_8g");
    float g = adxl355_raw_to_g(524287, ADXL355_RANGE_8G);
    float expected = 524287.0f * 0.0000156f;
    TEST_ASSERT(approx_eq(g, expected, 1e-6f), "raw 524287 @ 8g");
    TEST_END();
}

static void test_raw_to_mps2(void)
{
    TEST_START("raw_to_mps2");
    float mps2 = adxl355_raw_to_mps2(100000, ADXL355_RANGE_2G);
    float expected = 100000.0f * 0.0000039f * 9.80665f;
    TEST_ASSERT(approx_eq(mps2, expected, 1e-5f), "raw 100000 @ 2g -> m/s^2");
    TEST_END();
}

static void test_init_null_args(void)
{
    TEST_START("init_null_args");
    adxl355_t dev;
    adxl355_bus_t bus;
    memset(&bus, 0, sizeof(bus));
    TEST_ASSERT(adxl355_init(NULL, &bus) == ADXL355_ERR_NULL, "dev NULL");
    TEST_ASSERT(adxl355_init(&dev, NULL) == ADXL355_ERR_NULL, "bus NULL");
    TEST_END();
}

static void test_probe_bad_device(void)
{
    TEST_START("probe_bad_device");
    adxl355_mock_bus_t mock;
    adxl355_mock_bus_init(&mock);
    /* Don't set identity => probe should fail */
    adxl355_bus_t bus = adxl355_mock_bus_get_interface(&mock);
    adxl355_t dev;
    adxl355_init(&dev, &bus);
    TEST_ASSERT(adxl355_probe(&dev) == ADXL355_ERR_BAD_DEVICE, "bad device");
    TEST_END();
}

static void test_probe_ok(void)
{
    TEST_START("probe_ok");
    adxl355_mock_bus_t mock;
    adxl355_mock_bus_init(&mock);
    adxl355_mock_bus_set_identity_ok(&mock);
    adxl355_bus_t bus = adxl355_mock_bus_get_interface(&mock);
    adxl355_t dev;
    adxl355_init(&dev, &bus);
    TEST_ASSERT(adxl355_probe(&dev) == ADXL355_OK, "probe OK");
    TEST_ASSERT(dev.initialized == true, "dev.initialized should be true");
    TEST_END();
}

static void test_set_range_writes_expected_register(void)
{
    TEST_START("set_range_writes_expected_register");
    adxl355_mock_bus_t mock;
    adxl355_mock_bus_init(&mock);
    adxl355_mock_bus_set_identity_ok(&mock);
    adxl355_bus_t bus = adxl355_mock_bus_get_interface(&mock);
    adxl355_t dev;
    adxl355_init(&dev, &bus);
    adxl355_probe(&dev);

    adxl355_set_range(&dev, ADXL355_RANGE_2G);

    /* Verify the write was to the RANGE register */
    int found = 0;
    for (size_t i = 0; i < mock.call_count; i++) {
        if (mock.calls[i].is_write && mock.calls[i].reg == ADXL355_REG_RANGE) {
            found = 1;
            TEST_ASSERT(mock.calls[i].data == 0, "range register value should be 0 for 2G");
            break;
        }
    }
    TEST_ASSERT(found == 1, "write to RANGE register occurred");
    TEST_END();
}

static void test_read_raw_reads_9_bytes(void)
{
    TEST_START("read_raw_reads_9_bytes");
    adxl355_mock_bus_t mock;
    adxl355_mock_bus_init(&mock);
    adxl355_mock_bus_set_identity_ok(&mock);
    adxl355_mock_bus_set_xyz_raw(&mock, 10, -20, 30);
    adxl355_bus_t bus = adxl355_mock_bus_get_interface(&mock);
    adxl355_t dev;
    adxl355_init(&dev, &bus);
    adxl355_probe(&dev);

    adxl355_raw_xyz_t raw;
    adxl355_status_t status = adxl355_read_raw(&dev, &raw);
    TEST_ASSERT(status == ADXL355_OK, "read_raw should succeed");
    TEST_ASSERT(raw.x == 10, "x should be 10");
    TEST_ASSERT(raw.y == -20, "y should be -20");
    TEST_ASSERT(raw.z == 30, "z should be 30");
    TEST_END();
}

static void test_status_string(void)
{
    TEST_START("status_string");
    TEST_ASSERT(strcmp(adxl355_status_string(ADXL355_OK), "ADXL355_OK") == 0, "OK string");
    TEST_ASSERT(strcmp(adxl355_status_string(ADXL355_ERR_BUS), "ADXL355_ERR_BUS") == 0, "BUS string");
    TEST_ASSERT(adxl355_status_string((adxl355_status_t)-99) != NULL, "unknown returns something");
    TEST_END();
}

static void test_set_power_mode(void)
{
    TEST_START("set_power_mode");
    adxl355_mock_bus_t mock;
    adxl355_mock_bus_init(&mock);
    adxl355_mock_bus_set_identity_ok(&mock);
    adxl355_bus_t bus = adxl355_mock_bus_get_interface(&mock);
    adxl355_t dev;
    adxl355_init(&dev, &bus);
    adxl355_probe(&dev);

    /* Write to power ctl should succeed */
    TEST_ASSERT(adxl355_set_power_mode(&dev, ADXL355_POWER_MEASUREMENT) == ADXL355_OK, "set measurement mode");
    TEST_ASSERT(adxl355_set_power_mode(&dev, ADXL355_POWER_STANDBY) == ADXL355_OK, "set standby mode");
    TEST_END();
}

static void test_reset(void)
{
    TEST_START("reset");
    adxl355_mock_bus_t mock;
    adxl355_mock_bus_init(&mock);
    adxl355_mock_bus_set_identity_ok(&mock);
    adxl355_bus_t bus = adxl355_mock_bus_get_interface(&mock);
    adxl355_t dev;
    adxl355_init(&dev, &bus);

    TEST_ASSERT(adxl355_reset(&dev) == ADXL355_OK, "reset should succeed");

    /* Verify reset register was written */
    int found = 0;
    for (size_t i = 0; i < mock.call_count; i++) {
        if (mock.calls[i].is_write && mock.calls[i].reg == ADXL355_REG_RESET) {
            found = 1;
            TEST_ASSERT(mock.calls[i].data == ADXL355_RESET_CODE, "reset code 0x52");
            break;
        }
    }
    TEST_ASSERT(found == 1, "write to RESET register occurred");
    TEST_END();
}

/* ---------------------------------------------------------------------------
 * Main
 * --------------------------------------------------------------------------- */
int main(void)
{
    printf("ADXL355 C Test Suite\n");
    printf("====================\n");

    test_decode_raw20_zero();
    test_decode_raw20_positive_one();
    test_decode_raw20_positive_max();
    test_decode_raw20_negative_min();
    test_decode_raw20_negative_one();
    test_raw_to_g_2g();
    test_raw_to_g_4g();
    test_raw_to_g_8g();
    test_raw_to_mps2();
    test_init_null_args();
    test_probe_bad_device();
    test_probe_ok();
    test_set_range_writes_expected_register();
    test_read_raw_reads_9_bytes();
    test_status_string();
    test_set_power_mode();
    test_reset();

    printf("\n====================\n");
    printf("Results: %d/%d passed, %d failed\n",
           g_tests_pass, g_tests_run, g_tests_fail);

    return g_tests_fail > 0 ? EXIT_FAILURE : EXIT_SUCCESS;
}
