#!/bin/python3

'''
	
'''
def START ():
	def ADD_TO_SYSTEM_PATHS (PATHS):
		import pathlib
		from os.path import dirname, join, normpath
		import sys
		
		THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()	
		for PATH in PATHS:
			sys.path.insert (0, normpath (join (THIS_FOLDER, PATH)))

		return;

	ADD_TO_SYSTEM_PATHS ([ 
		'MODULES'
	])

	import CLIQUE	
	CLIQUE.START ()
	
	
'''
import requests
import json
r = requests.put (
	'http://127.0.0.1:1110', 
	data = json.dumps ({
		"START": "",
		"FIELDS": {}
	})
)
print (r.text)
'''

'''
import ENCHUFLA
ENCHUFLA.PLEASE ({
	"START": "",
	"FIELDS": {}
})
'''
import json

def PLEASE (
	DATA,
	PORT = '1110'
):
	import requests
	r = requests.put (
		f'http://127.0.0.1:{ PORT }', 
		data = json.dumps (DATA)
	)
	print (r.text)
	
	STATUS = json.loads (r.text)
	
	assert (STATUS ["GOOD"] == True)

	return