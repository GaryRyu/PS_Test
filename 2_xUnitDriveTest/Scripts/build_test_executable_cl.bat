:: One of below commands must be executed before building the test executable.
:: Visual Studio 2017
:: "C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Auxiliary\Build\vcvarsall.bat" x64
:: Visual Studio 2019
:: "C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC\Auxiliary\Build\vcvarsall.bat" x64
:: Visual Studio 2022
:: "C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvarsall.bat" x64
del /q *.o *.obj *.exe

cl.exe ..\Sources\src\myFile1.c ..\Sources\src\myFile2.c ..\Sources\src\myFile3.c ^
    /I ..\Sources\include ^
    ..\Tests\test_main.c ..\Tests\test1.c ..\Tests\test2.c ..\Tests\test3.c ^
    "C:\Polyspace Test\R2024a\polyspace\pstest\pstunit\src\pstunit.c" ^
    /I"C:\Polyspace Test\R2024a\polyspace\pstest\pstunit\include" ^
    /link /out:testrunner.exe
