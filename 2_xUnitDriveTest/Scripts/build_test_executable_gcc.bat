set PATH=C:\msys64\mingw64\bin;C:\msys64\usr\bin;%PATH%;

del /q *.o *.obj *.exe

gcc ..\Sources\src\myFile1.c ..\Sources\src\myFile2.c ..\Sources\src\myFile3.c ^
    -I ..\Sources\include ^
    ..\Tests\test_main.c ..\Tests\test1.c ..\Tests\test2.c ..\Tests\test3.c ^
    "C:\Polyspace Test\R2024a\polyspace\pstest\pstunit\src\pstunit.c" ^
    -I "C:\Polyspace Test\R2024a\polyspace\pstest\pstunit\include" ^
    -o testrunner
