

'''
	python3 STATUS.py "/STATS/AGGREGATE_PC_RATIO/STATUS/STATUS_2.py"
'''

'''
	SOURCES:
		https://www.nasdaq.com/market-activity/stocks/fslr/option-chain
'''


import OPTIONS_CALC.STATS.AGGREGATE_PC_RATIO as AGGREGATE_PC_RATIO

def SCAN_JSON_PATH (PATH):
	import json

	import pathlib
	FIELD = pathlib.Path (__file__).parent.resolve ()

	from os.path import dirname, join, normpath
	import sys
	
	FULL_PATH = normpath (join (FIELD, PATH))
	
	with open (FULL_PATH) as SELECTOR:
		NOTE = json.load (SELECTOR)
	
	return NOTE



def CHECK_1 ():
	EXAMPLE = SCAN_JSON_PATH ("EXAMPLES/2.JSON")
	EVALUATION = AGGREGATE_PC_RATIO.CALC (EXAMPLE)
	
	import json
	print ("EVALUATION:", json.dumps (EVALUATION, indent = 4))

	assert (EVALUATION ["EXPIRATIONS"][0]["SUMS"]["PUTS"]["ASK"] == 2000)
	assert (EVALUATION ["EXPIRATIONS"][0]["SUMS"]["PUTS"]["BID"] == 1200)
	assert (EVALUATION ["EXPIRATIONS"][0]["SUMS"]["PUTS"]["LAST"] == 0)

	assert (EVALUATION ["EXPIRATIONS"][0]["SUMS"]["CALLS"]["ASK"] == 2000)
	assert (EVALUATION ["EXPIRATIONS"][0]["SUMS"]["CALLS"]["BID"] == 1700)
	assert (EVALUATION ["EXPIRATIONS"][0]["SUMS"]["CALLS"]["LAST"] == 3600)

	assert (EVALUATION ["EXPIRATIONS"][0]["PC RATIOS"]["ASK"] == [ 1, 1 ])
	assert (EVALUATION ["EXPIRATIONS"][0]["PC RATIOS"]["BID"] == [ 1, 1.4166666666666667 ])
	assert (EVALUATION ["EXPIRATIONS"][0]["PC RATIOS"]["LAST"] == [ "~>= INFINITY", 0 ])

	assert (EVALUATION ["PC RATIOS"]["ASK"] == [ 1, 1 ])
	assert (EVALUATION ["PC RATIOS"]["BID"] == [ 1, 1.4166666666666667 ])
	assert (EVALUATION ["PC RATIOS"]["LAST"] == [ "~>= INFINITY", 0 ])

	assert (EVALUATION ["SUMS"]["PUTS"]["ASK"] == 2000)
	assert (EVALUATION ["SUMS"]["PUTS"]["BID"] == 1200)
	assert (EVALUATION ["SUMS"]["PUTS"]["LAST"] == 0)

	assert (EVALUATION ["SUMS"]["CALLS"]["ASK"] == 2000)
	assert (EVALUATION ["SUMS"]["CALLS"]["BID"] == 1700)
	assert (EVALUATION ["SUMS"]["CALLS"]["LAST"] == 3600)

	return;
	
	
CHECKS = {
	"CHECK 1": CHECK_1
}