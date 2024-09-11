
#include <stdio.h>

#include "myApp.h"
#include "pstunit.h"

/* Custom data structure for the parameterized tests */
typedef struct  {
  int input1;
  int input2;
  int expectedResult;
} test_param_t;

/* Custom formatter */
void pst_format_param_test_param_t(char *buff, const pst_size_t param_size,
                                   const void *param) {
  (void)param_size;
  pst_format(buff, PST_PARAM_IDX_BUFF_SIZE, "in1:%d, in2:%d, res:%d",
             (*PST_STATIC_CAST(test_param_t *, param)).input1,
             (*PST_STATIC_CAST(test_param_t *, param)).input2,
             (*PST_STATIC_CAST(test_param_t *, param)).expectedResult);
}

test_param_t test_data[] = {
    /* input1 input2 expectedResult */
    {0, 0, 0},
    {-1, 5, 0},
    {1, 6, 7},
    {99, 6, 105},
    {100, -8, 92},
    {101, 6, 0}
};

PST_PARAM_WITH_VALUES(test_param, test_param_t,
                      pst_format_param_test_param_t, test_data, 6);

PST_SUITE(mySuite2);

PST_TEST_CONFIG(mySuite2, test1) {
    PST_ADD_PARAM(test_param);
};

PST_TEST_BODY(mySuite2, test1) {
  int arg1 = (PST_PARAM_PTR(test_param))->input1;
  int arg2 = (PST_PARAM_PTR(test_param))->input2;
  int expectedResult = (PST_PARAM_PTR(test_param))->expectedResult;
  int retValue = functionToTest(arg1, arg2);
  PST_VERIFY(expectedResult == retValue);
}

PST_REGFCN(registerSuite2) {
    PST_ADD_TEST(mySuite2, test1);
}
