set PATH=%PATH%;"C:\Polyspace Test\R2024a\polyspace\bin";

del /q instrumented_code *.o *.obj *.exe

@echo Instrumenting the source files and Compiling the source codes only
@echo cl.exe /c option compiles only. It does not link object files.
polyspace-code-profiler -instrument ^
                        -instrum-dir .\instrumented_code\ ^
                        -limit-instrumentation-to ..\Src ^
                        -cov-metric-level mcdc ^
                        -- ^
                        cl.exe /c ..\Src\algo.c ..\Src\saturate.c tests.c stubs.c ^
                        "C:\Polyspace Test\R2024a\polyspace\pstest\pstunit\src\pstunit.c" ^
                        -I ..\Header ^
                        -I "C:\Polyspace Test\R2024a\polyspace\pstest\pstunit\include"


@echo Linking the object files with the precompiled library
cl.exe algo.obj saturate.obj tests.obj stubs.obj pstunit.obj ^
    "C:\Polyspace Test\R2024a\polyspace\psprofile\lib\win64\import\microsoft\libmwpsprofile_cli_runtime.lib" ^
    /link /out:covrunner.exe


@echo Collecting coverage data from the executable, covrunner.exe
polyspace-code-profiler -run ^
                        -instrum-dir .\instrumented_code ^
                        -results-dir .\coverage_results ^
                        -- ^
                        covrunner.exe -color


@echo Generating coverage report
polyspace-code-profiler -report -report-dir .\reports\ -html .\coverage_results\