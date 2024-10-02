/**
 * Polyspace example.
 *       Copyright 2012-2023 The MathWorks, Inc.
 */

#ifndef SINGLE_FILE_ANALYSIS_H
#define SINGLE_FILE_ANALYSIS_H

#include <stdint.h>

#define NA_VALUE (-128)

/* public interface */
int8_t generic_validation(int8_t extrapolated_speed, uint8_t computed_speed);

#endif
