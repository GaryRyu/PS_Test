#include "myApp.h"

int functionToTest(int arg1, int arg2) {
   if ((arg1 >= 0) && (arg1 <= 100)) {
      return arg1 + arg2;
   } else {
      return 0;
   }
}