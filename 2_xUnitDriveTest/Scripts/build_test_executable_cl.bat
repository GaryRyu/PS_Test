:: One of below commands must be executed before building the test executable.
:: Visual Studio 2017
:: "C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Auxiliary\Build\vcvarsall.bat" x64
:: Visual Studio 2019
:: "C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC\Auxiliary\Build\vcvarsall.bat" x64
:: Visual Studio 2022
:: "C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvarsall.bat" x64
del /q *.o *.obj *.exe

cl.exe ..\Src\algo.c ..\Src\saturate.c ^
    /I ..\Header ^
    tests.c stubs.c ^
    "C:\Polyspace Test\R2024b_Prerelease\polyspace\pstest\pstunit\src\pstunit.c" ^
    /I"C:\Polyspace Test\R2024b_Prerelease\polyspace\pstest\pstunit\include" ^
    /link /out:testrunner.exe
