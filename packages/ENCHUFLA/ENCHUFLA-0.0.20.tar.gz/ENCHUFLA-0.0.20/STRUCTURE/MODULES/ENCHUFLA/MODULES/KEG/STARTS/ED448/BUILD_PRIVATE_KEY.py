

'''
import requests
import json
r = requests.put (
	'http://127.0.0.1:1110', 
	data = json.dumps ({
		"START": "BUILD ED448 PRIVATE KEY",
		"FIELDS": {
			"SEED": "5986888b11358bf3d541b41eea5daece1c6eff64130a45fc8b9ca48f3e0e02463c99c5aedc8a847686d669b7d547c18fe448fc5111ca88f4e8",
			"PATH": "ED448_PRIVATE_KEY.DER"
		}
	})
)
print (r.text)
'''
def BUILD_PRIVATE_KEY (
	FIELDS
):
	SEED = FIELDS ["SEED"]
	PATH = FIELDS ["PATH"]

	#print ("SEED:", SEED)
	#print ("PATH:", PATH)
	
	from DUOM.ED448.PRIVATE_KEY.CREATE import CREATE_PRIVATE_KEY
	PRIVATE_KEY = CREATE_PRIVATE_KEY (
		SEED, 
		"DER",
		PATH = PATH 
	)
	if (PRIVATE_KEY ["GOOD"] == False):
		return {
			"GOOD": False
		}
	
	return {
		"GOOD": True
	}