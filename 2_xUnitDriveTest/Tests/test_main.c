#include "pstunit.h"

#ifndef PSTEST_BUILD
int main(int argc, char *argv[]) {
    PST_REGFCN_CALL(registerSuite1);
    PST_REGFCN_CALL(registerSuite2);
    PST_REGFCN_CALL(registerSuite3);

    return PST_MAIN(argc, argv);
}
#endif