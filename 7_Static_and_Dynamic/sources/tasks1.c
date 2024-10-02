/**
 * Polyspace example.
 *       Copyright 2012-2020 The MathWorks, Inc.
 */

#include "include.h"

typedef struct {
    int A;
    int B;
} rec;

/* Global variables */
int PowerLevel = 0;

static rec SHR4;
static int SHR5 = 5;
static int SHR = 0;
static int SHR2 = 0;
static int SHR6;


int orderregulate(void) {
    int tmp, X;
    Increase_PowerLevel();
    SHR4.A = 22;
    tmp = PowerLevel + SHR4.A;

    X = tmp;
    return X;
}


static void initregulate(void) {
    int tmp = 0;
    while (random_int() < 1000) {
        tmp = orderregulate();
        Begin_CS();
        tmp = SHR + SHR2 + SHR6;
        End_CS();
        tmp = Get_PowerLevel();
        Compute_Injection();
    } /* end loop; */
}


void tregulate(void) {
    if (random_int() > 0) {
        initregulate();
    }

    while (random_int() > 0) {
        orderregulate();
    }
}


static void Tserver(void) {
    int I = 1;
    SHR2 = 22;
    orderregulate();
    while (I < 10000) {
        I = I + 1;
        Begin_CS();
        SHR = 22 + SHR6;
        End_CS();
        Exec_One_Cycle(I);
    }
    SHR2 = 0;
}


void server2(void) {
    Tserver();
}


void server1(void) {
    Tserver();
}


void proc1(void) {
    SHR5 = SHR5 + 23;
}


void proc2(void) {
    static int SHR3 = 0;

    SHR4.B = 22;
    SHR3 = SHR3 + 1 + SHR4.B + SHR5;
}
