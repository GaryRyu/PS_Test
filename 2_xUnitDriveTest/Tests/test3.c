#include "pstunit.h"

#include "myApp.h"

PST_SUITE(mySuite3);

PST_TEST(mySuite3, test1) {
    int retValue = otherFunctionToTest(100);
    PST_VERIFY(5 == retValue);
}
/* Error: miss many tests */

PST_REGFCN(registerSuite3) {
    PST_ADD_TEST(mySuite3, test1);
}