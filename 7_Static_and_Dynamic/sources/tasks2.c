/**
 * Polyspace example.
 *       Copyright 2012-2023 The MathWorks, Inc.
 */

#include "include.h"


/* Internal function         */
/* Needed for MISRA-rule 8.1 */
static void Computing_from_Sensors(int i, int j);
static void Command_Ordering(int X);
static void Pilot_Balance(int X);
static void Sequencer(int X);


void Increase_PowerLevel(void) {
    PowerLevel++;
}


static void Computing_from_Sensors(int i, int j) {
    int loc = i + j;
    if (loc < 0) {
        loc++;
    }
}


void Compute_Injection(void) {
    static int Injection;

    Computing_from_Sensors(PowerLevel, Injection);
}


int Get_PowerLevel(void) {
    int Tmp;
    Tmp = PowerLevel;
    return Tmp;
}


static void Command_Ordering(int X) {
    volatile int loc = 0;
    X = loc;
    if (X == 12) {
        loc = orderregulate();
    }
}


static void Pilot_Balance(int X) {
    Command_Ordering(X);
}


static void Sequencer(int X) {
    Command_Ordering(X);
}


void Exec_One_Cycle(int X) {
    Pilot_Balance(X);
    Sequencer(X);
}


/* Critical sections */
void Begin_CS(void) {}


void End_CS(void) {}
