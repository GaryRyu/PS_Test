# -*- coding: utf-8 -*-

import os, sys, logging
from datetime import datetime
# Add Polyspace Test Installation folder to PATH
sys.path.append(r"C:\Polyspace Test\R2024b\bin\win64")
# Load the polyspace.project and polyspace.test modules
import polyspace.project, polyspace.test # type: ignore

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def loadTestResult(psTestResultFilePath):
    try:
        if os.path.exists(psTestResultFilePath):
            if os.path.isfile(psTestResultFilePath):
                return polyspace.test.TestResults(psTestResultFilePath)
            else:
                logging.error(f"\033[33m{psTestResultFilePath} is not a file.\033[0m")
    except Exception as e:
        logging.error(f"\033[31mError loading Polyspace Test results: {e}\033[0m")


def loadProfilingResult(psProfilingResultFilePath):
    try:
        if os.path.exists(psProfilingResultFilePath):
            if os.path.isfile(psProfilingResultFilePath):
                return polyspace.test.ProfilingResults(psProfilingResultFilePath)
            else:
                logging.error(f"\033[33m{psProfilingResultFilePath} is not a file.\033[0m")
    except Exception as e:
        logging.error(f"\033[31mError loading Polyspace Test Profiling results: {e}\033[0m")
        

def ratioOfTestsPassed(testResult):
    try:
        # polyspace.test.TestResults 타입과 polyspace.test.TestSuiteResult 타입만 처리 가능
        if isinstance(testResult, polyspace.test.TestResults):
            # 전체 Test 수 대비 성공한 Test cases의 개수 비율
            return ((testResult.TestsPassed / testResult.TestsRequested) * 100)
        elif isinstance(testResult, list) and isinstance(testResult[0], polyspace.test.TestSuiteResult):
            # testResult변수가 Test Suite인 경우, 각각의 Test Suite의 이름과 성공/요청 비율 정보를 전달
            return [[item.Name, (item.TestsPassed / item.TestsRequested) * 100] for item in testResult]
        else:
            logging.error("\033[31mThe type is not TestResults or TestSuiteResults.\033[0m")
    except Exception as e:
        logging.error(f"\033[31mFailed to calculate the ratio about TestsPassed / TestsRequested: {e}\033[0m")


def ratioOfTestsFailed(testResult):
    try:
        # polyspace.test.TestResults 타입과 polyspace.test.TestSuiteResult 타입만 처리 가능
        if isinstance(testResult, polyspace.test.TestResults):
            # 전체 Test 수 대비 실패한 Test cases의 개수 비율
            return ((testResult.TestsFailed / testResult.TestsRequested) * 100)
        elif isinstance(testResult, list) and isinstance(testResult[0], polyspace.test.TestSuiteResult):
            # testResult변수가 Test Suite인 경우, 각각의 Test Suite의 이름과 실패/요청 비율 정보를 전달
            return [[item.Name, (item.TestsFailed / item.TestsRequested) * 100] for item in testResult]
        else:
            logging.error("\033[31mThe type is not TestResults or TestSuiteResults.\033[0m")
    except Exception as e:
        logging.error(f"\033[31mFailed to calculate the ratio about TestsFailed / TestsRequested: {e}\033[0m")


def ratioOfTestsIncompleted(testResult):
    try:
        # polyspace.test.TestResults 타입과 polyspace.test.TestSuiteResult 타입만 처리 가능
        if isinstance(testResult, polyspace.test.TestResults):
            # 전체 Test 수 대비 완료하지 못 한 Test cases의 개수 비율
            return ((testResult.TestsIncomplete / testResult.TestsRequested) * 100)
        elif isinstance(testResult, list) and isinstance(testResult[0], polyspace.test.TestSuiteResult):
            # testResult변수가 Test Suite인 경우, 각각의 Test Suite의 이름과 완료실패/요청 비율 정보를 전달
            return [[item.Name, (item.TestsIncomplete / item.TestsRequested) * 100] for item in testResult]
        else:
            logging.error("\033[31mThe type is not TestResults or TestSuiteResults.\033[0m")
    except Exception as e:
        logging.error(f"\033[31mFailed to calculate the ratio about TestsIncompleted / TestsRequested: {e}\033[0m")


def covMetricsFromProfilingResult(profilingResult, metricsType):
    try:
        # 선택한 Coverage Metrics 타입이 문자열인지, profilingResult가 polyspace.test.ProfilingResults 타입인지 검사. 타입이 맞지 않으면 에러
        if isinstance(metricsType, str) and isinstance(profilingResult, polyspace.test.ProfilingResults):
            covMetrics = profilingResult.Coverage.getCoverageInfo(metricsType)
            if covMetrics.TotalCount:
                return (((covMetrics.CoveredCount + covMetrics.JustifiedCount) / covMetrics.TotalCount) * 100)
            else:
                logging.error("\033[31mCoverage was not calculated.\033[0m")
        else:
            logging.error("\033[31mThe type is not ProfilingResults for 1st arg or Str for 2nd arg.\033[0m")
    except Exception as e:
        logging.error(f"\033[31mFailed to return the value for a specific coverage metrics: {e}\033[0m")


def main():
    # Test 결과물 저장할 때 Profiling 결과까지 함께 저장했다면 .pstestr 파일이 있는 위치에 codecov-data-files 폴더가 생김
    # 해당 Test 결과물을 로드하면 Profiling 결과까지 결과물 변수(반환값)에 함께 같이 로드됨
    psTestResult = loadTestResult(".\\1_GUI_Driven_Test\\"+"testResult_"+datetime.now().strftime("%Y%m%d")+".pstestr")
    
    ratioAllTestPassed = ratioOfTestsPassed(psTestResult)
    ratioAllTestFailed = ratioOfTestsFailed(psTestResult)
    ratioAllTestIncompleted = ratioOfTestsIncompleted(psTestResult)
    logging.info("============= Summary Test Information for all test cases =============")
    logging.info(f"Ratio of Test Passed: {ratioAllTestPassed:.2f}%")
    logging.info(f"Ratio of Test Failed: {ratioAllTestFailed:.2f}%")
    logging.info(f"Ratio of Test Incompleted: {ratioAllTestIncompleted:.2f}%")

    if (ratioAllTestIncompleted > 0) or (ratioAllTestFailed > 10) or (ratioAllTestPassed < 90):
        logging.error(f"\033[31mFailed to meet the threshold for test cases.\033[0m")
        # sys.exit(1)

    ratioTestSuitesPassed = ratioOfTestsPassed(psTestResult.TestSuiteResults)
    ratioTestSuitesFailed = ratioOfTestsFailed(psTestResult.TestSuiteResults)
    ratioTestSuitesIncompleted = ratioOfTestsIncompleted(psTestResult.TestSuiteResults)
    
    logging.info("============= Summary Test Information for each specific test suite =============")
    for element in ratioTestSuitesPassed:
        logging.info(f"Ratio of Test Passed: {element[1]}% in {element[0]} suite")
    for element in ratioTestSuitesFailed:
        logging.info(f"Ratio of Test Failed: {element[1]}% in {element[0]} suite")
    for element in ratioTestSuitesIncompleted:
        logging.info(f"Ratio of Test Incompleted: {element[1]}% in {element[0]} suite")

    if (any([ratio for ratio in ratioTestSuitesIncompleted if ratio[1] > 0]) or 
        any([ratio for ratio in ratioTestSuitesFailed if ratio[1] > 10]) or 
        any([ratio for ratio in ratioTestSuitesPassed if ratio[1] < 90])):
        logging.error(f"\033[31mFailed to meet the threshold for test suites.\033[0m")
        # sys.exit(1)
    
    # 지원하는 타입 - 'statement', 'decision', 'condition', 'mcdc', 'function', 'function call', 'function exit'
    statementMetrics = covMetricsFromProfilingResult(psTestResult.Profiling, 'statement')
    decisionMetrics = covMetricsFromProfilingResult(psTestResult.Profiling, 'decision')
    conditionMetrics = covMetricsFromProfilingResult(psTestResult.Profiling, 'condition')
    mcdcMetrics = covMetricsFromProfilingResult(psTestResult.Profiling, 'mcdc')
    functionMetrics = covMetricsFromProfilingResult(psTestResult.Profiling, 'function')
    functionCallMetrics = covMetricsFromProfilingResult(psTestResult.Profiling, 'function call')
    functionExitMetrics = covMetricsFromProfilingResult(psTestResult.Profiling, 'function exit')

    logging.info("============= Summary Coverage Information of all test cases =============")
    logging.info(f"Statement Coverage: {statementMetrics:.2f}%")
    logging.info(f"Decision Coverage: {decisionMetrics:.2f}%")
    logging.info(f"Condition Coverage: {conditionMetrics:.2f}%")
    logging.info(f"MCDC Coverage: {mcdcMetrics:.2f}%")
    logging.info(f"Function Coverage: {functionMetrics:.2f}%")
    logging.info(f"Function Call Coverage: {functionCallMetrics:.2f}%")
    logging.info(f"Function Exit Coverage: {functionExitMetrics:.2f}%")
    
    if (statementMetrics < 60) or (decisionMetrics < 60) or (conditionMetrics < 60) or (mcdcMetrics < 60) or (functionMetrics < 60) or (functionCallMetrics < 60) or (functionExitMetrics < 60):
        logging.error(f"\033[31mFailed to meet the threshold, 60% for each coverage metrics.\033[0m")
        sys.exit(1)

if __name__ == "__main__":
    main()