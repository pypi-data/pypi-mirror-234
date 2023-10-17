
'''
	import OPTIONS_CALC.STATS.AGGREGATE_PC_RATIO as AGGREGATE_PC_RATIO
	EVALUATION = AGGREGATE_PC_RATIO.CALC (EXAMPLE_1)
	
	import json
	print ("EVALUATION:", json.dumps (EVALUATION, indent = 4))
'''

'''
	{
		"EXPIRATIONS": [{
			"EXPIRATION": "2023-10-27",
			"SUMS": {
				"PUTS": {
					"ASK":
					"BID":
					"LAST"
				},
				"CALLS": {
					"ASK":
					"BID":
					"LAST"
				}
			},
			"PC RATIOS": {
				"ASK":
				"BID":
				"LAST"
			}
		}],
		"SUMS": {
			"PUTS": {
				"ASK":
				"BID":
				"LAST"
			},
			"CALLS": {
				"ASK":
				"BID":
				"LAST"
			}
		},
		"PC RATIOS": {
			"ASK":
			"BID":
			"LAST"
		}
	}
'''

from OPTIONS_CALC.TOOLS.RATIO import CALC_RATIO

import pydash
def RETURN_NUMBER (OBJECT, PATH, DEFAULT):
	FOUND = pydash.get (
		OBJECT,
		PATH,
		DEFAULT
	)
	
	TYPE = type (FOUND)
	if (TYPE == int or TYPE == float):
		return FOUND
		
	if (FOUND == None):
		return DEFAULT;

	print ("FOUND WAS NOT ACCOUNTED FOR:", FOUND)
	raise Exception (f"FOUND WAS NOT ACCOUNTED FOR: { FOUND }")
		
	return DEFAULT

def RETRIEVE_MULTIPLICAND (STRIKE):
	return STRIKE ["CONTRACT SIZE"] * STRIKE ["OPEN INTEREST"]
 
	try:
		pass;
	
	except Exception as E:
		pass;
		

def EQUALITY_CHECK (PARAM_1, PARAM_2):
	try:
		assert (PARAM_1 == PARAM_2)
	except Exception as E:
		import traceback
		
		print ("PARAM 1", PARAM_1)
		print ("PARAM 2", PARAM_2)	
		
		print (traceback.print_exception (E))

		raise Exception (E)

	return
	

def CALC (CHAIN):
	EXPIRATIONS = CHAIN ["EXPIRATIONS"]
	
	EVALUATION = {
		"EXPIRATIONS": [],
		"SUMS": {
			"PUTS": {
				"ASK": 0,
				"BID": 0,
				"LAST": 0
			},
			"CALLS": {
				"ASK": 0,
				"BID": 0,
				"LAST": 0
			}
		},
		"PC RATIOS": {
			"ASK": 0,
			"BID": 0,
			"LAST": 0
		}
	}
	
	
	for EXPIRATION in EXPIRATIONS:
		CALLS_STRIKES = EXPIRATION ["CALLS"]["STRIKES"]
		PUTS_STRIKES = EXPIRATION ["PUTS"]["STRIKES"]
		
		EXPIRATION_NOTE = {
			"EXPIRATION": EXPIRATION ["EXPIRATION"],
			"SUMS": {
				"PUTS": {
					"ASK": 0,
					"BID": 0,
					"LAST": 0
				},
				"CALLS": {
					"ASK": 0,
					"BID": 0,
					"LAST": 0
				}
			},
			"PC RATIOS": {
				"ASK": 0,
				"BID": 0,
				"LAST": 0
			}
		}
		
		EQUALITY_CHECK (len (CALLS_STRIKES), len (PUTS_STRIKES))
		
		DIRECTION = "CALLS"
		for STRIKE in CALLS_STRIKES:		
			EXPIRATION_NOTE ["SUMS"][ DIRECTION ]["ASK"] += RETURN_NUMBER (STRIKE, [ "PRICES", "ASK" ], 0) * RETRIEVE_MULTIPLICAND (STRIKE)
			EXPIRATION_NOTE ["SUMS"][ DIRECTION ]["BID"] += RETURN_NUMBER (STRIKE, [ "PRICES", "BID" ], 0) * RETRIEVE_MULTIPLICAND (STRIKE)
			EXPIRATION_NOTE ["SUMS"][ DIRECTION ]["LAST"] += RETURN_NUMBER (STRIKE, [ "PRICES", "LAST" ], 0) * RETRIEVE_MULTIPLICAND (STRIKE)
		
		DIRECTION = "PUTS"
		for STRIKE in PUTS_STRIKES:		
			EXPIRATION_NOTE ["SUMS"][ DIRECTION ]["ASK"] += RETURN_NUMBER (STRIKE, [ "PRICES", "ASK" ], 0) * RETRIEVE_MULTIPLICAND (STRIKE)
			EXPIRATION_NOTE ["SUMS"][ DIRECTION ]["BID"] += RETURN_NUMBER (STRIKE, [ "PRICES", "BID" ], 0) * RETRIEVE_MULTIPLICAND (STRIKE)
			EXPIRATION_NOTE ["SUMS"][ DIRECTION ]["LAST"] += RETURN_NUMBER (STRIKE, [ "PRICES", "LAST" ], 0) * RETRIEVE_MULTIPLICAND (STRIKE)
		
		EXPIRATION_NOTE ["PC RATIOS"]["ASK"] = CALC_RATIO (
			EXPIRATION_NOTE ["SUMS"][ "PUTS" ]["ASK"],
			EXPIRATION_NOTE ["SUMS"][ "CALLS" ]["ASK"]
		)
		EXPIRATION_NOTE ["PC RATIOS"]["BID"] = CALC_RATIO (
			EXPIRATION_NOTE ["SUMS"][ "PUTS" ]["BID"],
			EXPIRATION_NOTE ["SUMS"][ "CALLS" ]["BID"]
		)
		EXPIRATION_NOTE ["PC RATIOS"]["LAST"] = CALC_RATIO (
			EXPIRATION_NOTE ["SUMS"][ "PUTS" ]["LAST"],
			EXPIRATION_NOTE ["SUMS"][ "CALLS" ]["LAST"]
		)
		
		EVALUATION ["SUMS"][ "CALLS" ]["ASK"] += RETURN_NUMBER (EXPIRATION_NOTE, [ "SUMS", "CALLS", "ASK" ], 0)
		EVALUATION ["SUMS"][ "CALLS" ]["BID"] += RETURN_NUMBER (EXPIRATION_NOTE, [ "SUMS", "CALLS", "BID" ], 0)
		EVALUATION ["SUMS"][ "CALLS" ]["LAST"] += RETURN_NUMBER (EXPIRATION_NOTE, [ "SUMS", "CALLS", "LAST" ], 0)
		
		EVALUATION ["SUMS"][ "PUTS" ]["ASK"] += RETURN_NUMBER (EXPIRATION_NOTE, [ "SUMS", "PUTS", "ASK" ], 0)
		EVALUATION ["SUMS"][ "PUTS" ]["BID"] += RETURN_NUMBER (EXPIRATION_NOTE, [ "SUMS", "PUTS", "BID" ], 0)
		EVALUATION ["SUMS"][ "PUTS" ]["LAST"] += RETURN_NUMBER (EXPIRATION_NOTE, [ "SUMS", "PUTS", "LAST" ], 0)
		
		EVALUATION ["EXPIRATIONS"].append (EXPIRATION_NOTE)
		
	EVALUATION ["PC RATIOS"]["ASK"] = CALC_RATIO (
		EVALUATION ["SUMS"][ "PUTS" ]["ASK"],
		EVALUATION ["SUMS"][ "CALLS" ]["ASK"]
	)
	
	EVALUATION ["PC RATIOS"]["BID"] = CALC_RATIO (
		EVALUATION ["SUMS"][ "PUTS" ]["BID"],
		EVALUATION ["SUMS"][ "CALLS" ]["BID"]
	)
	
	EVALUATION ["PC RATIOS"]["LAST"] = CALC_RATIO (
		EVALUATION ["SUMS"][ "PUTS" ]["LAST"],
		EVALUATION ["SUMS"][ "CALLS" ]["LAST"]
	)

	return EVALUATION