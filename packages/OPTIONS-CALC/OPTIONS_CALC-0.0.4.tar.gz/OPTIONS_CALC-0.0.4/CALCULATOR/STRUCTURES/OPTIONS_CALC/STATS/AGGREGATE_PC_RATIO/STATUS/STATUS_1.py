

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
	EXAMPLE_1 = SCAN_JSON_PATH ("EXAMPLES/1.JSON")

	#print ("EXAMPLE 1", EXAMPLE_1)

	EVALUATION = AGGREGATE_PC_RATIO.CALC (EXAMPLE_1)
	
	import json
	print ("EVALUATION:", json.dumps (EVALUATION, indent = 4))

	return;
	
	
CHECKS = {
	"CHECK 1": CHECK_1
}