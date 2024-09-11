#include "pstunit.h"

#include "myApp.h"

PST_SUITE(mySuite1);

PST_TEST(mySuite1, test1) {
    int retValue = myAbs(3);
    PST_VERIFY(3 == retValue);
}

PST_TEST(mySuite1, test2_NOK) {
    int retValue = myAbs(-6);
    int expValue = -6;         /* Error: Bad copy/paste */
    PST_VERIFY_EQ_INT_MSG(retValue, expValue, "This test should fail");
}
PST_REGFCN(registerSuite1) {
    PST_ADD_TEST(mySuite1, test1);
    PST_ADD_TEST(mySuite1, test2_NOK);
}