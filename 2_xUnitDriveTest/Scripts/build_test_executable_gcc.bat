set PATH=%PATH%;C:\msys64\mingw64\bin;C:\msys64\usr\bin

del /q *.o *.obj *.exe

gcc ..\Src\algo.c ..\Src\saturate.c ^
    -I ..\Header ^
    tests.c stubs.c ^
    "C:\Polyspace Test\R2024b_Prerelease\polyspace\pstest\pstunit\src\pstunit.c" ^
    -I "C:\Polyspace Test\R2024b_Prerelease\polyspace\pstest\pstunit\include" ^
    -o testrunner
