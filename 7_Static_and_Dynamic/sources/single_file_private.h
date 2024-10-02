/**
 * Polyspace example.
 *       Copyright 2012-2023 The MathWorks, Inc.
 */

#ifndef SINGLE_FILE_PRIVATE_H
#define SINGLE_FILE_PRIVATE_H

#include <assert.h>

#define BIN0 1
#define BIN1 2
#define BIN2 4
#define BIN3 8
#define BIN4 16
#define BIN5 32
#define BIN6 64
#define BIN7 128
#define BIN8 256
#define BIN9 512
#define BIN10 1024
#define BIN11 2048
#define BIN12 4096
#define BIN13 8192
#define BIN14 16484
#define BIN15 32768

#define BIN_v0 (BIN10)
#define BIN_v1 (BIN8)
#define BIN_v2 (BIN5)
#define BIN_v3 (BIN2)
#define BIN_v4 (BIN3)
#define BIN_v5 (BIN4)

#define binVALUE(x) (BIN_##x)
#define gVALUE(x) ((int)(x) / binVALUE(x))
#define pVALUE(x, value) ((value)*binVALUE(x))


#define all_values(_type)                                   \
    static _type all_values_##_type(_type min, _type max);  \
    static _type all_values_##_type(_type min, _type max) { \
        volatile _type tmp##_type;                          \
        _type ret;                                          \
        ret = tmp##_type;                                   \
        assert((ret >= min) && (ret <= max));               \
        return ret;                                         \
    }

#endif
