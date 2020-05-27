import socket
import cv2

class NetworkCamDriverClient():
	def __init__(self):
		self.Height=0
		self.Width=0
		self.BytesPerPixel=0
		self.sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.isconnected = False
		
	#public void Connect(string server, int port)
	def Connect(self, server, port):
		try:
			self.sck.settimeout(60)
			self.sck.connect((server, port))
			self.sck.settimeout(None)

			data = self.sck.recv(11)

			if data[0]!=0xFF:
				print("Unexpected header: Needed 0xff command start, got ", hex(data[0]))

			if data[1]!=0x02:
				print("Unexpected header: Needed 0x02 command start, got ", hex(data[1]))

			self.Width = (data[2] << 24) | (data[3] << 16) | (data[4] << 8) | data[5]
			self.Height = (data[6] << 24) | (data[7] << 16) | (data[8] << 8) | data[9]
			self.BytesPerPixel = int((data[10] + 7) / 8)

			#print('Received', repr(data))
			#print('Virtualcam Request Width', self.Width)
			#print('Virtualcam Height', self.Height)
			#print('Virtualcam BytesPerPixel', self.BytesPerPixel)

			self.isconnected = True
			return True;
			
		except socket.error as msg:
			print("Unable to Connect : ", msg)
			self.isconnected = False
			return False;
		
	#public async Task SendImage(ReadOnlySpan<byte> image)
	def SendImage(self, frame):
		
		tmpframe = cv2.flip(frame, 0)
		tmpframe = cv2.resize(tmpframe, (self.Width, self.Height))
		
		size = (self.Width*self.Height)*self.BytesPerPixel
				
		header = bytearray(5)
		header[0]=255
		header[1]=1
		header[2]=(size & 0xFF)
		header[3]=((size >> 8) & 0xFF)
		header[4]=((size >> 16) & 0xFF)

		#print('Send Header')
		self.sck.send(header)

		#print('Send Imagedata')
		self.sck.send(tmpframe.data)