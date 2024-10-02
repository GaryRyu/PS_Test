/**
 * Polyspace example.
 *       Copyright 2012-2023 The MathWorks, Inc.
 */

#include "single_file_analysis.h"
#include "single_file_private.h"
#include "include.h"

/*
   global variables declaration
   input variables for the module/function/file
*/
uint16_t v0;
int16_t v1;
int16_t v2;
uint8_t v3;
int16_t v4;
int16_t v5;

/* output variables for the module/function/file */
static int32_t output_v6;
static int32_t output_v7;
static int8_t output_v1;

static int16_t saved_values[127];

/* function definitions */
all_values(int32_t);
all_values(int16_t);
all_values(uint16_t);

/* Internal function         */
/* Needed for MISRA-rule 8.1 */
void functional_ranges(void) {	
    /*  sets all global variables to their functional range */
    v0 = all_values_uint16_t(0 * BIN_v0, 90 * BIN_v0);

    v1 = all_values_int16_t(0 * BIN_v1, 90 * BIN_v1);
    v2 = all_values_int16_t(-810 * BIN_v2, 150 * BIN_v2);
    v3 = (uint8_t)all_values_int32_t(0 * BIN_v3, 54 * BIN_v3);
    v4 = all_values_int16_t(-45 * BIN_v4, 126 * BIN_v4);

    v5 = all_values_int16_t(-90 * BIN_v5, 900 * BIN_v5);
}


static int32_t new_speed(int32_t in, int8_t ex_speed, uint8_t c_speed) {
    return (in / 9 + ((int32_t)ex_speed + (int32_t)c_speed) / 2);
}


static char reset_temperature(uint8_t in_v3) {
    int array[255 - (54 * BIN_v3)];

    array[in_v3 - 255] = 0;
    return array[in_v3 - 255];
}


int8_t generic_validation(int8_t extrapolated_speed, uint8_t computed_speed) {
    /**************************************************************
     * Input parameters                                           *
     *           NAME                      POSSIBLE VALUES        *
     *      int8_t extrapolated_speed              [ -128 ; 127 ]     *
     *      uint8_t computed_speed                  [    0 ; 255 ]     *
     **************************************************************
     * Output values                                              *
     *           NAME                      POSSIBLE VALUES        *
     *      int8_t ret               NA_VALUE (-128), or [ -46; 126 ] *
     **************************************************************/
    int32_t int32_t_ret;
    int16_t v0_c;
    int8_t int8_t_ret;

    /*  sets all global variables to their functional range */
    functional_ranges();

    v0_c = (int16_t)gVALUE(v0);
    if (v0_c == 90) {
        return (int8_t)NA_VALUE;
        /* grey explanation
         * when initialized, v0 is truncated to [ 0 ; 26624]
         * instead of [ 0 ; 92160 ] (92160 = 90 * BIN_v0)
         *
         * Note:
         *        90 * BIN_v0 = 90 * 1024 = 92160
         *        and  92160 MOD [ 0 ; 65535] = 26624
         */
    }

    if (v1 >= 60 * BIN_v1) {
        output_v6 = gVALUE(v2) * gVALUE(v4) / gVALUE(v1);
    } else {
        output_v6 = gVALUE(v3) * gVALUE(v1) - gVALUE(v5);
    }

    output_v7 = new_speed(output_v6, extrapolated_speed, computed_speed);
    int32_t_ret = new_speed(output_v7, extrapolated_speed, computed_speed) / 2;

    int8_t_ret = (int8_t)NA_VALUE;
    /* the return value spec indicates that it should be between [ -50 ; 126 ] */
    if ((int32_t_ret < -50) || (int32_t_ret > 126)) {
        /* if dead code, we can remove this test
         *   - gain in execution speed
         *   - gain for the other developers who don't need to test the return
         *     value against NA_VALUE (-128)
         */
        SEND_MESSAGE(int32_t_ret, "%d out of functional bounds reached");
    } else {
        int8_t_ret = (int8_t)int32_t_ret;
        output_v1 = int8_t_ret + 15;
    }

    if (output_v7 >= 0) {

#pragma Inspection_Point output_v7 int8_t_ret
        saved_values[output_v7] = int8_t_ret;
        return int8_t_ret;
    }
    return reset_temperature(v3);
}


static int32_t unused_fonction(void) {
    return saved_values[output_v1] +
           (int32_t)generic_validation((output_v6 / 10000), (output_v7 / 16000));
}
