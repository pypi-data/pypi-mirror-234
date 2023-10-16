


from .STARTS import STARTS

from flask import Flask, request
import json

from QR.GENERATE import GENERATE_QR

RECORDS = 0

def TAP (
	PORT = 0
):
	app = Flask (__name__)

	'''
		STRATEGY:
			ENCHUFLA SEND "{ 'START': 'BUILD ED448 PRIVATE KEY', 'FIELDS': { 'PATH': 'ED448_PRIVATE_KEY.DER' } }"
	'''

	'''
		curl -X PUT localhost:5000 -d "{ 'START': 'BUILD ED448 PRIVATE KEY', 'FIELDS': { 'PATH': 'ED448_PRIVATE_KEY.DER' } }"
		curl -X PUT localhost:5000 -d '{ "START": "BUILD ED448 PRIVATE KEY" }'
		curl -X PUT localhost:5000 -d '{ "START": "BUILD ED448 PRIVATE KEY", "FIELDS": { "PATH": "ED448_PRIVATE_KEY.DER", "SEED": "4986888B11358BF3D541B41EEA5DAECE1C6EFF64130A45FC8B9CA48F3E0E02463C99C5AEDC8A847686D669B7D547C18FE448FC5111CA88F4E8" } }'
	'''
	@app.route ("/", methods = [ 'PUT' ])
	def ROUTE ():
		DATA = ""
		
		try:
			DATA = request.get_data ();
			if (RECORDS >= 1): print ("--- DATA ::", DATA)
			
			UTF8 = DATA.decode ('utf-8')
			if (RECORDS >= 1): print ("UTF8 ::", UTF8)
			
			JSON = json.loads (UTF8)
			if (RECORDS >= 1): print ("JSON ::", json.dumps (UTF8))
			if (RECORDS >= 1): print ("JSON ::", type (JSON))

			START = JSON ["START"]
			if (RECORDS >= 1): print ("START ::", START)
			
			FIELDS = JSON ["FIELDS"]
			if (RECORDS >= 1): print ("FIELDS ::", FIELDS)
			
			START = STARTS (
				START = START,
				FIELDS = FIELDS
			)
			if (START ["GOOD"] == True):
				return json.dumps (START), 999
				return json.dumps ({ "GOOD": True }), 999
			
			ALARM = ""
			if ("ALARM" in START):
				ALARM = START ["ALARM"]
		
			return json.dumps ({ "GOOD": False, "ALARM": ALARM }), 701
			
		except Exception as E:
			import traceback
			traceback.print_exception (E)
		
		
		return json.dumps ({ "GOOD": False }), 702

	
	
	app.run (
		port = PORT
	)
	
	return;
	
	'''
		curl -X PUT localhost:5000 -d "{  }"
		
		curl -X PUT localhost:5000 -d "{}" -H "Content-Type: application/json"
	'''
	@app.route ("/", methods = [ 'PUT' ])
	def BUILD_PRIVATE_KEY ():
		#data = request.form.get ('data')
		data = request.get_data ()

		print ("DATA:", request.data)
	
		#from DUOM.ED448.PRIVATE_KEY.BUILD import BUILD_PRIVATE_KEY
		#[ PRIVATE_KEY, PRIVATE_KEY_EXPORT ] = BUILD_PRIVATE_KEY (SEED, FORMAT)
	
		return "<p>PUT</p>"	
	
	@app.route ("/QR")
	def QR ():
		QR_CODE = GENERATE_QR (
			STRING = 'THIS IS A QR CODE MESSAGE!'
		)
	
		return f"""
<body style="background: #222">
	<img src='{ QR_CODE }' />
</body>
		"""
		
	app.run ()