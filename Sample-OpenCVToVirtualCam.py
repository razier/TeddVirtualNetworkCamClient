import cv2
from Razier.TeddVirtualNetworkCamClient import NetworkCamDriverClient

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

client = NetworkCamDriverClient()
client.Connect("127.0.0.1", 9090);

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

while(True):
	ret, frame = cap.read()
	frame = cv2.resize(frame, (0, 0), fx=0.50, fy=0.50)
	
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.1, 4)

	for (x, y, w, h) in faces:
		cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 1)

	cv2.imshow('frame',frame)
	if client.isconnected == True:
		client.SendImage(frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()