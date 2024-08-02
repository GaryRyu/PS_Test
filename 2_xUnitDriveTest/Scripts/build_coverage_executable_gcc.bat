set PATH=%PATH%;C:\msys64\mingw64\bin;C:\msys64\usr\bin;"C:\Polyspace Test\R2024b_Prerelease\polyspace\bin";

del /q instrumented_code *.o *.obj *.exe

@echo Instrumenting the source files and Compiling the source codes only
@echo gcc -c option compiles only. It does not link object files.
polyspace-code-profiler -instrument -instrum-dir .\instrumented_code\ ^
                        -limit-instrumentation-to ..\Src -cov-metric-level mcdc ^
                        -- gcc -c ..\Src\algo.c ..\Src\saturate.c tests.c stubs.c ^
                        "C:\Polyspace Test\R2024b_Prerelease\polyspace\pstest\pstunit\src\pstunit.c" ^
                        -I ..\Header -I "C:\Polyspace Test\R2024b_Prerelease\polyspace\pstest\pstunit\include"


@echo Linking the object files with the precompiled library
gcc -o covrunner algo.o saturate.o tests.o stubs.o pstunit.o ^
    "C:\Polyspace Test\R2024b_Prerelease\polyspace\psprofile\lib\win64\import\mingw64\libmwpsprofile_cli_runtime.lib"


@echo Collecting coverage data from the executable, covrunner.exe
polyspace-code-profiler -run -instrum-dir .\instrumented_code\ ^
                        -results-dir .\coverage_results\ ^
                        -- covrunner.exe -color


@echo Generating coverage report
polyspace-code-profiler -report -report-dir .\reports\ -html .\coverage_results\
