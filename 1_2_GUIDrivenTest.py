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

    # Build and Run Tests
    res = polyspace.test.run(psProject)

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
    
    psProject.close()

else:
    print(f"{psProjectName} file does not exist. Cannot step forward.")
    sys.exit()

