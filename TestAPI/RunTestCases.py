import requests
import json
from CovidDataProvider.Config import Config


def run_testCase(url,expectedResults):
    
    response = requests.get(url)
    assert (response.text == expectedResults or  (str(response.json()) == str(expectedResults)))
    
if __name__ == '__main__':

	with open(Config.TC_PATH) as f:
	    TestCases = json.load(f)
	TotalTestCases = len(TestCases)
	PassedTestCases = 0
	for test in TestCases:
	    try:
	        run_testCase(TestCases[test]['url'],TestCases[test]['res'])
	        print('Passed testcase: {} Description: {} url: {} '.format(test,TestCases[test]['Description'],TestCases[test]['url']))
	        PassedTestCases += 1
	    except:
	        print('Failed testcase: {} Description: {} url: {} '.format(test,TestCases[test]['Description'],TestCases[test]['url']))

	print ("{} out of {} test cases passed".format(PassedTestCases,TotalTestCases))