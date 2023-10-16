

import qrcode
from io import BytesIO
from base64 import b64encode

def GENERATE_QR (
	STRING = ''
):
	QR_CODE_IMG = qrcode.make (STRING)
	
	BUFFER = BytesIO ()
	QR_CODE_IMG.save (BUFFER)
	
	BUFFER.seek (0)
	ENCODED_IMG = b64encode (BUFFER.read ()).decode ()
	
	QR_CODE_BASE_64 = f'data:image/png;base64,{ENCODED_IMG}'
	
	return QR_CODE_BASE_64;