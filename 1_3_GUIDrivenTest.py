import sys

# Add Polyspace Test Installation folder to PATH
sys.path.append(r"C:\Polyspace Test\R2024b_Prerelease\bin\win64")

# Load the polyspace.project and polyspace.test modules
import polyspace.project
import polyspace.test
import os

psProjectName = "1_GUIDrivenTest.psprjx"

if os.path.exists(os.path.join('1_GUIDrivenTest',psProjectName)):
    print(f"{psProjectName} file exists.")

    # Load project
    psProject = polyspace.project.Project(os.path.join('1_GUIDrivenTest',psProjectName))
    
    # Set the coverage metric level to CONDITION_DECISION
    psProject.ActiveTestConfiguration.CoverageOptions.Level = polyspace.project.CoverageMetricLevel.MCDC

    # Build and Run Tests with Code Coverage
    res = polyspace.test.run(psProject, ProfilingSelection=polyspace.test.ProfilingSelection.COVERAGE)

    # Check overall status of test execution
    if not res.Status.Failed and not res.Status.Incomplete: 
        print("All tests have passed.")
    elif res.Status.Failed:
        print("At least one test failed.")
    else:
        print("At least one test did not run to completion.")

    # Print names of suites with failing tests
    for resTestSuite in res.TestSuiteResults:
        if resTestSuite.Status.Failed:
            print(f"Failed test suite is {resTestSuite.Name}")

    # Print file names and line numbers of failing assessments
    for resTestSuite in res.TestSuiteResults:
        if resTestSuite.Status.Failed:
            for resTestCase in resTestSuite.TestCaseResults:
                if resTestCase.Status.Failed:
                    print(f"Failed test case is {resTestSuite.Name}/{resTestCase.Name}\n")
                    for resAssessment in resTestCase.FailedAssessmentResults:
                        print(f"Failed test is located at {resAssessment.File}: Line {resAssessment.Line}")
                        
else:
    print(f"{psProjectName} file does not exist. Cannot step forward.")
    sys.exit()

# Read coverage results
profilingResults = res.Profiling
coverageResults = profilingResults.Coverage
coverage_metrics = ['decision','condition','mcdc','statement','function call','function', 'function exit']

# Show pass/fail status of coverage results based on coverage percentage
print("Coverage Threshold is 50%")
for metric in coverage_metrics:
    metric_details = coverageResults.getCoverageInfo(metric)
    if metric_details.TotalCount:
        pct = (metric_details.CoveredCount + metric_details.JustifiedCount) / metric_details.TotalCount
        print(f"{metric} coverage is {pct:.2%}\n ", " (FAIL)" if pct < 0.5 else " (PASS)")
    else:
        print(f"{metric} coverage not calculated\n")


psProject.close()
    