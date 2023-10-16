

'''
import requests
import json
r = requests.put (
	'http://127.0.0.1:1110', 
	data = json.dumps ({
		"START": "BUILD ED448 PRIVATE KEY",
		"FIELDS": {
			"PRIVATE KEY PATH": "",
			"PUBLIC KEY PATH": "",
			"PUBLIC KEY FORMAT": "DER"
		}
	})
)
print (r.text)
'''
def BUILD_PUBLIC_KEY (
	FIELDS
):
	from DUOM.ED448.PUBLIC_KEY.CREATE import CREATE_PUBLIC_KEY
	PUBLIC_KEY = CREATE_PUBLIC_KEY ({
		"PRIVATE KEY PATH": FIELDS ["PRIVATE KEY PATH"],
		"PUBLIC KEY PATH": FIELDS ["PUBLIC KEY PATH"],
		"PUBLIC KEY FORMAT": "DER"
	})
	if (PUBLIC_KEY ["GOOD"] == False):
		return {
			"GOOD": False
		}
	
	return {
		"GOOD": True
	}