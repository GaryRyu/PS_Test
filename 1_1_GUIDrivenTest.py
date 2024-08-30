import sys

# Add Polyspace Test Installation folder to PATH
sys.path.append(r"C:\Polyspace Test\R2024b_Prerelease\bin\win64")

# Load the polyspace.project and polyspace.test modules
import polyspace.project
import polyspace.test
import os

psProjectName = "GuiDrivenTest.psprjx"

if os.path.exists(psProjectName):
    print(f"{psProjectName} file exists.")

    # Load project
    psProject = polyspace.project.Project(psProjectName)

else:
    print(f"{psProjectName} file does not exist.")

    # Create project
    psProject = polyspace.project.Project(psProjectName)

    # Add source files
    psProject.Code.Files.add(os.path.join('1_GUIDrivenTest','Sources','src','myFile1.c'))
    psProject.Code.Files.add(os.path.join('1_GUIDrivenTest','Sources','src','myFile2.c'))
    psProject.Code.Files.add(os.path.join('1_GUIDrivenTest','Sources','src','myFile3.c'))

    # Add include paths
    psProject.IncludePaths.add(os.path.join('1_GUIDrivenTest','Sources','include'))

    # Add test files
    psProject.Tests.Files.add(os.path.join('1_GUIDrivenTest','Tests','test1.c'))
    psProject.Tests.Files.add(os.path.join('1_GUIDrivenTest','Tests','test2.c'))
    psProject.Tests.Files.add(os.path.join('1_GUIDrivenTest','Tests','test3.c'))
    
    # Save the project (If you do not save, you will lose the project.)
    psProject.save()

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