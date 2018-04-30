"""Abstracts communication using the Xbee."""
import logging
import json
import serial

class Communication:
	"""Class abstracting communication using the Xbee via serial."""
	def __init__(self, port, time_out):
		print(".")
		self.logger = logging.getLogger(__name__)
		self.ser = serial.Serial(port, timeout=time_out)

	def send(self, data):
		"""Send data via the communication module.
		This functions sends the data via serial. It is important that the data
		be "jsonnable" or else this will fail miserably.
		:param data: The data to send (must be able to be jsonned).
		"""
		# json data given by user and string encode it
		jsoned = json.dumps(data)
		byte_data = str.encode(jsoned)
		# send data
		self.ser.write(byte_data)
		self.ser.write(b'\n')

	def receive(self):
		"""Receive data from the communcation module.
		This function is currently blocking until data has been received. The
		type of data returned should be the same as the type that was sent by
		the other device.
		:returns:
		None -- if the time_out time is exceeded
		original data -- This data has the type that was sent. It is
								   up to the user to determine the type and use
								   it accordingly.
		"""
		jsoned_data = self.ser.readline()
		if not jsoned_data:
			return None
		try:
			unjsoned_data = json.loads(jsoned_data)
			return unjsoned_data
		except ValueError as err:
			self.logger.warn('ValueError: {}'.format(err))
			self.logger.warn('received: {}'.format(jsoned_data))
			return None					
		
		#TESTING STUFF
		#return {"x":50,"y":50,"z":50,"lat":33.5,"lon":87.5,"temp":25,"time":datetime.datetime.now()}
		#return "This is your string"