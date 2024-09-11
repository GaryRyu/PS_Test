set PATH=C:\msys64\mingw64\bin;C:\msys64\usr\bin;"C:\Polyspace Test\R2024a\polyspace\bin";%PATH%;

del /q instrumented_code *.o *.obj *.exe

@echo Instrumenting the source files and Compiling the source codes only
@echo gcc -c option compiles only. It does not link object files.
polyspace-code-profiler -instrument -instrum-dir .\instrumented_code\ ^
                        -limit-instrumentation-to ..\Sources -cov-metric-level mcdc ^
                        -- gcc -c ..\Sources\src\myFile1.c ..\Sources\src\myFile2.c ..\Sources\src\myFile3.c ^
                        ..\Tests\test_main.c ..\Tests\test1.c ..\Tests\test2.c ..\Tests\test3.c ^
                        "C:\Polyspace Test\R2024a\polyspace\pstest\pstunit\src\pstunit.c" ^
                        -I ..\Sources\include -I "C:\Polyspace Test\R2024a\polyspace\pstest\pstunit\include"


@echo Linking the object files with the precompiled library
gcc -o covrunner myFile1.o myFile2.o myFile3.o test_main.o test1.o test2.o test3.o pstunit.o ^
    "C:\Polyspace Test\R2024a\polyspace\psprofile\lib\win64\import\mingw64\libmwpsprofile_cli_runtime.lib"


@echo Collecting coverage data from the executable, covrunner.exe
polyspace-code-profiler -run -instrum-dir .\instrumented_code\ ^
                        -results-dir .\coverage_results\ ^
                        -- covrunner.exe -color


@echo Generating coverage report
polyspace-code-profiler -report -report-dir .\reports\ -html .\coverage_results\
