/**
 * Polyspace example.
 *       Copyright 2012-2023 The MathWorks, Inc.
 */

#include <stdbool.h>
#include <stdint.h>

#include "include.h"
#include "single_file_analysis.h"

/* hardware ports */
volatile int8_t PORT_A;
volatile uint8_t PORT_B;

int interpolation(void) {
    int i, item = 0;
    int found = false;


    for (i = 0; i < MAX_SIZE; i++) {
        arr++;
        if ((found == false) && (*arr > 16)) {
            found = true;
            item = i;
        }
    }
    *arr = 20;
    return item;
}

#ifndef PSTEST_BUILD
int main(void) {
    int temp;
    PowerLevel = -10000;

    RTE();

    initialise_current_data();

    temp = read_on_bus();
    switch (temp) {
    case new_move:
        temp = interpolation();
        break;
    case previous_move:
        generic_validation(PORT_A, PORT_B);
        break;
    default:
        compute_new_coordonates();
        polynomia(55);
        polynomia(3);
        break;
    }
    return 0;
}

#endif /* End of PSTEST_BUILD */