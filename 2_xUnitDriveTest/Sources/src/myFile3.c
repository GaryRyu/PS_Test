#include "myApp.h"


int otherFunctionToTest(int arg1) {
   arg1 = myAbs(arg1);
   if (arg1 >= 500) {
      return 1;
   } else if (arg1 >= 400) {
      return 2;
   } else if (arg1 >= 300) {
      return 3;
   } else if (arg1 >= 200) {  
      return 4;
   } else if (arg1 >= 100) {
      return 5;
   } else if (arg1 >= 0) {
      return 6;
   } else {
      return 0;
   }
}
