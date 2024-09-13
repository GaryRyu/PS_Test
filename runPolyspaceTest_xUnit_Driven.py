# -*- coding: utf-8 -*-

import os, sys, logging
from datetime import datetime
# Add Polyspace Test Installation folder to PATH
if os.name == 'nt':
    if os.path.exists(r"C:\Polyspace Test\R2024b\bin\win64"):
        sys.path.append(r"C:\Polyspace Test\R2024b\bin\win64")
    else:
        logging.error(f"\033[31mCould not find a path for Polyspace Test\033[0m")
elif os.name == 'posix':
    if os.path.exists(r"/usr/local/Polyspace_Test/R2024b/bin/glnxa64"):
        sys.path.append(r"/usr/local/Polyspace_Test/R2024b/bin/glnxa64")
    else:
        logging.error(f"\033[31mCould not find a path for Polyspace Test\033[0m")
else:
    logging.error(f"\033[31mPolyspace Test does not support this OS\033[0m")
# Load the polyspace.project and polyspace.test modules
import polyspace.project, polyspace.test # type: ignore

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

STATEMENT = polyspace.project.CoverageMetricLevel.STATEMENT
DECISION = polyspace.project.CoverageMetricLevel.DECISION
CONDITION_DECISION = polyspace.project.CoverageMetricLevel.CONDITION_DECISION
MCDC = polyspace.project.CoverageMetricLevel.MCDC


def createPolyspaceProject(psProjectName):
    global psProject, scriptDir, projectDir
    try:
        if os.path.exists(psProjectName):
            logging.info(f"\033[0m{psProjectName} exists. Loading it ...")
        else:
            logging.info(f"\033[0m{psProjectName} does not exist. Creating it ...")
            
        psProject = polyspace.project.Project(psProjectName)
        # 아래 함수들에서 상대 경로로 파일/폴더 위치를 저장하므로 디렉토리 위치를 변경할 필요가 있음
        scriptDir = os.getcwd()
        os.chdir(os.path.dirname(psProject.Path))
        projectDir = os.getcwd()
        logging.info(f"\033[0mChanged the current directory to {projectDir}.")
    except Exception as e:
        logging.error(f"\033[31mError in creating/loading project: {e}\033[0m")
        sys.exit(1)


def changeToolchain(toolName):
    try:
        psProject.ActiveBuildConfiguration.Toolchain = toolName
    except Exception as e:
        logging.error(f"\033[31mError changing toolchain: {e}\033[0m")


def saveProject():
    try:
        psProject.save()
    except Exception as e:
        logging.error(f"\033[31mError saving project: {e}\033[0m")
        

def closeProject():
    try:
        psProject.close()
    except Exception as e:
        logging.error(f"\033[31mError closing project: {e}\033[0m")


def resAbsPathFromProject(fileFolderPath):
    try:
        if not os.path.isabs(fileFolderPath):
            # 상대 경로인 경우, projectDir을 기준으로 절대 경로로 변환
            fileFolderPath = os.path.join(projectDir, fileFolderPath)
        return os.path.abspath(fileFolderPath)
    except Exception as e:
        logging.error(f"\033[31mError resolving absolute path for file or folder from PROJECT file: {e}\033[0m")


def resAbsPathFromScript(fileFolderPath):
    try:
        if not os.path.isabs(fileFolderPath):
            # 상대 경로인 경우, scriptDir을 기준으로 절대 경로로 변환
            fileFolderPath = os.path.join(scriptDir, fileFolderPath)
        return os.path.abspath(fileFolderPath)
    except Exception as e:
        logging.error(f"\033[31mError resolving absolute path for file or folder from SCRIPT file: {e}\033[0m")


def checkExistence(itemsList, fileOrFolerPath):
    try:
        if os.path.isfile(fileOrFolerPath):
            return any (
                    os.path.exists(resAbsPathFromProject(item)) and
                    os.stat(resAbsPathFromProject(item)).st_ino == os.stat(fileOrFolerPath).st_ino
                    for item in itemsList
                )
        else:
            return any (
                    os.path.exists(resAbsPathFromProject(item.Path)) and
                    os.stat(resAbsPathFromProject(item.Path)).st_ino == os.stat(fileOrFolerPath).st_ino
                    for item in itemsList
                )
    except Exception as e:
        logging.error(f"\033[31mError during checking if a file or folder exists in the list of the Project: {e}\033[0m")


def addSrcFileOrFolder(srcFileOrFolder):
    try:
        absPathSrcFileOrFolder = resAbsPathFromScript(srcFileOrFolder)
        if os.path.exists(absPathSrcFileOrFolder):
            if os.path.isfile(absPathSrcFileOrFolder):
                # 파일 목록에 이미 동일한 파일이 있는지 검사
                # Code.Files.add() 함수는 에러를 발생시켜서 코드 실행이 멈춤
                fileExist = checkExistence(list(psProject.Code.Files), absPathSrcFileOrFolder)
                
                if fileExist:
                    logging.warning(f"\033[33mSource file {srcFileOrFolder} already exists in the list.\033[0m")
                else:
                    # 스크립트의 위치, 프로젝트 생성 위치, 상대 경로로 지정한 소스 파일들의 위치가 다를 수 있어, 프로젝트 파일 위치를 기준으로 소스 파일/폴더 경로 조정 필요
                    relativeSrcPath = os.path.relpath(resAbsPathFromScript(srcFileOrFolder), projectDir)
                    psProject.Code.Files.add(relativeSrcPath)
            else:
                # 폴더 목록에 이미 동일한 폴더가 있는지 검사
                # Code.Folders.add() 함수는 에러를 발생시켜서 코드 실행이 멈춤
                folderExist = checkExistence(list(psProject.Code.Folders), absPathSrcFileOrFolder)
    
                if folderExist:
                    logging.warning(f"\033[33mSource folder {srcFileOrFolder} already exists in the list.\033[0m")
                else:
                    # 스크립트의 위치, 프로젝트 생성 위치, 상대 경로로 지정한 소스 파일들의 위치가 다를 수 있어, 프로젝트 파일 위치를 기준으로 소스 파일/폴더 경로 조정 필요
                    relativeSrcPath = os.path.relpath(resAbsPathFromScript(srcFileOrFolder), projectDir)
                    psProject.Code.Folders.add(relativeSrcPath)
                    psProject.refreshSources()
        else:
            logging.warning(f"\033[33mSource file/folder {srcFileOrFolder} does not exist.\033[0m")
    except Exception as e:
        logging.error(f"\033[31mError during adding source file or folder in the Project: {e}\033[0m")
        
        
def addTestSrcFileOrFolder(srcFileOrFolder):
    try:
        absPathSrcFileOrFolder = resAbsPathFromScript(srcFileOrFolder)
        if os.path.exists(absPathSrcFileOrFolder):
            if os.path.isfile(absPathSrcFileOrFolder):
                # 파일 목록에 이미 동일한 파일이 있는지 검사
                # Code.Files.add() 함수는 에러를 발생시켜서 코드 실행이 멈춤
                fileExist = checkExistence(list(psProject.Tests.Files), absPathSrcFileOrFolder)
                
                if fileExist:
                    logging.warning(f"\033[33mTest source file {srcFileOrFolder} already exists in the list.\033[0m")
                else:
                    # 스크립트의 위치, 프로젝트 생성 위치, 상대 경로로 지정한 소스 파일들의 위치가 다를 수 있어, 프로젝트 파일 위치를 기준으로 소스 파일/폴더 경로 조정 필요
                    relativeSrcPath = os.path.relpath(resAbsPathFromScript(srcFileOrFolder), projectDir)
                    psProject.Tests.Files.add(relativeSrcPath)
            else:
                # 폴더 목록에 이미 동일한 폴더가 있는지 검사
                # Code.Folders.add() 함수는 에러를 발생시켜서 코드 실행이 멈춤
                folderExist = checkExistence(list(psProject.Tests.Folders), absPathSrcFileOrFolder)
    
                if folderExist:
                    logging.warning(f"\033[33mTest source folder {srcFileOrFolder} already exists in the list.\033[0m")
                else:
                    # 스크립트의 위치, 프로젝트 생성 위치, 상대 경로로 지정한 소스 파일들의 위치가 다를 수 있어, 프로젝트 파일 위치를 기준으로 소스 파일/폴더 경로 조정 필요
                    relativeSrcPath = os.path.relpath(resAbsPathFromScript(srcFileOrFolder), projectDir)
                    psProject.Tests.Folders.add(relativeSrcPath)
                    psProject.refreshSources()
        else:
            logging.warning(f"\033[33mTest source file/folder {srcFileOrFolder} does not exist.\033[0m")
    except Exception as e:
        logging.error(f"\033[31mError during adding test source file or folder in the Project: {e}\033[0m")
        

def addIncPath(incPath):
    try:
        absIncPath = resAbsPathFromScript(incPath)
        if os.path.exists(absIncPath):
            if os.path.isfile(absIncPath):
                # 파일 경로는 include path에 추가될 수 없음
                logging.warning(f"\033[33mFile {incPath} cannot be added in the include path.\033[0m")
            else:
                # 폴더 목록에 이미 동일한 폴더가 있는지 검사
                # IncludePaths.add() 함수는 프로젝트에 중복으로 동일한 내용을 추가함
                folderExist = checkExistence(list(psProject.IncludePaths), absIncPath)
                
                if folderExist:
                    logging.warning(f"\033[33mInclude path {incPath} already exists in the list.\033[0m")
                else:
                    relativeIncPath = os.path.relpath(resAbsPathFromScript(incPath), projectDir)
                    psProject.IncludePaths.add(relativeIncPath)
        else:
            # 지정한 폴더가 없어도 include path에 추가되는 현상이 있음. 문제될 것은 없지만 의미가 없으므로 경로는 추가하지 않고 메시지 출력
            logging.warning(f"\033[33mInclude path {incPath} does not exist.\033[0m")
    except Exception as e:
        logging.error(f"\033[31mError during adding include path in the Project: {e}\033[0m")


def setCoverageMetricsLevel(covMetricsLvl):
    try:
        psProject.ActiveTestConfiguration.CoverageOptions.Level = covMetricsLvl
    except TypeError:
        logging.error(f"\033[31mThe value, {covMetricsLvl} is not the type, polyspace.project.CoverageMetricLevel\033[0m")
    except Exception as e:
        logging.error(f"\033[31mError during adding include path in the Project: {e}\033[0m")


def buildTestExec():
    try:
        status = polyspace.test.build(psProject)
        return status
    except Exception as e:
        logging.error(f"\033[31mFailed to build for Test: {e}\033[0m")

    
def buildCoverageExec():
    try:
        status = polyspace.test.build(psProject, ProfilingSelection=polyspace.test.ProfilingSelection.COVERAGE)
        return status
    except Exception as e:
        logging.error(f"\033[31mFailed to build for Coverage: {e}\033[0m")

    
def rebuildTestExec():
    try:
        status = polyspace.test.build(psProject, ForceRebuild=True)
        return status
    except Exception as e:
        logging.error(f"\033[31mFailed to rebuild for Test: {e}\033[0m")
    

def rebuildCoverageExec():
    try:
        status = polyspace.test.build(psProject, ForceRebuild=True, ProfilingSelection=polyspace.test.ProfilingSelection.COVERAGE)
        return status
    except Exception as e:
        logging.error(f"\033[31mFailed to rebuild for Coverage: {e}\033[0m")

        
def runTestExec():
    try:
        testResults = polyspace.test.run(psProject)
        return testResults
    except Exception as e:
        logging.error(f"\033[31mFailed to run test exectuable for Test: {e}\033[0m")

    
def runCoverageExec():
    try:
        testResults = polyspace.test.run(psProject, ProfilingSelection=polyspace.test.ProfilingSelection.COVERAGE)
        return testResults
    except Exception as e:
        logging.error(f"\033[31mFailed to run test exectuable for Coverage: {e}\033[0m")


def main():
    # 프로젝트 설정 시작 - 이미 파일이 존재하면 로드를 진행하고, 없으면 새로 생성할 수 있음.
    # os.path.join()과 같은 함수를 사용할 것이 아니라면 'r' prefix 를 넣어줘야 함.
    createPolyspaceProject(r".\2_xUnit_Driven_Test\2_xUnitDrivenTest.psprjx")
    
    # 소스 파일이나 소스 폴더 추가하기
    # 기존 프로젝트에 이미 추가되어 있었다면 추가할 필요는 없음
    # os.path.join()과 같은 함수를 쓸 것이 아니라면, 문자열 앞에 'r' prefix를 붙여줘야 함
    addSrcFileOrFolder(os.path.join('2_xUnit_Driven_Test','Sources','src'))
    addSrcFileOrFolder(r".\2_xUnit_Driven_Test\Sources\src\myFile1.c")
    addSrcFileOrFolder(r".\2_xUnit_Driven_Test\Sources\src\myFile2.c")
    addSrcFileOrFolder(os.path.join('2_xUnit_Driven_Test','Sources','src','myFile3.c'))
    
    # 헤더를 위한 Include 경로 추가
    # 기존 프로젝트에 이미 추가되어 있었다면 추가할 필요는 없음
    addIncPath(os.path.join('2_xUnit_Driven_Test','Sources','include'))
    
    # Test case 관련 소스 코드 추가
    # 기존 프로젝트에 원하는 Test case들이 추가되어 있었다면 할 필요는 없음
    addTestSrcFileOrFolder(os.path.join('2_xUnit_Driven_Test','Tests'))
    
    # 측정할 커버리지 메트릭스 선택 -  STATEMENT, DECISION, CONDITION_DECISION, MCDC
    # setCoverageMetricsLevel(STATEMENT)
    # setCoverageMetricsLevel(DECISION)
    # setCoverageMetricsLevel(CONDITION_DECISION)
    setCoverageMetricsLevel(MCDC)

    # 스크립트 수행하는 OS에 따라 빌드 툴체인 변경
    if os.name == 'nt':
        # "MinGW64 | CMake/gmake (64-bit Windows)"
        # "MinGW64 | CMake/Ninja (64-bit Windows)"
        # "MinGW64 | gmake (64-bit Windows)"
        # "Microsoft Visual C++ 2022 v17.0 | CMake/nmake (64-bit Windows)"
        # "Microsoft Visual C++ 2019 v16.0 | nmake (64-bit Windows)"
        changeToolchain("MinGW64 | gmake (64-bit Windows)")
    elif os.name == 'posix':
        # "GNU gcc/g++ | CMake/gmake (64-bit Linux)"
        # "GNU gcc/g++ | CMake/Ninja (64-bit Linux)"
        # "GNU gcc/g++ | gmake (64-bit Linux)"
        changeToolchain("GNU gcc/g++ | gmake (64-bit Linux)")
    else:
        logging.error(f"\033[31mPolyspace Test does not support the OS.\033[0m")

    # 정보를 저장해 두고 싶다면 프로젝트 파일로 저장
    # 꼭 할 필요는 없으나 차후 프로젝트 정보를 GUI상에서 열어보려면 필요함 (Build를 진행하면 저장됨)
    saveProject()
    
    # Build (Optional) - True 또는 False로만 빌드 결과 반환
    # stat = buildTestExec()
    stat = buildCoverageExec()
    # stat = rebuildTestExec()
    # stat = rebuildCoverageExec()
    
    if stat == False:
        logging.error(f"\033[31mFailed to build\033[0m")
        closeProject()
        sys.exit(1)
    
    # Run - 빌드 과정이 없어도 Run 수행시 테스트용 실행 파일이 없으면 빌드가 이루어짐
    # testResults = runTestExec()
    covResults = runCoverageExec()
    
    # Save - 만들어진 분석 결과물을 저장
    covResults.save("testResult_" + datetime.now().strftime("%Y%m%d"))

if __name__ == "__main__":
    main()