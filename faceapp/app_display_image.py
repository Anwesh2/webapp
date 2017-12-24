import cv2
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline 
import os
from uuid import uuid4
from shutil import copyfile
from flask import Flask, request, render_template, send_from_directory

__author__ = 'anwesh'

app = Flask(__name__)

kejriwal = "no" # presence of kejriwal
modi = "no" # presence of modi
presence_of_face = "no" # presence of a face
p = 0  # number of faces


APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
	global kejriwal
	global modi
	global presence_of_face
	global p
	global gray

	target1 = os.path.join(APP_ROOT, 'edited_images/')
	#target2 = os.path.join(APP_ROOT, 'edited_images/')

	if not os.path.isdir(target1):
            os.mkdir(target1)
	else:
		print("Couldn't create upload directory: {}".format(target1))

	#if not os.path.isdir(target2):
	#	os.mkdir(target2)
	#else:
	#	print("Couldn't create upload directory: {}".format(target2))

	#print(request.files.getlist("file"))

	for upload in request.files.getlist("file"):
		#print(upload)
		#print("{} is the file name".format(upload.filename))
		filename = upload.filename
		destination1 = target1 + filename
		#destination2 = target2 + filename
		#print ("Accept incoming file:", filename)
		#print ("Save it to:", destination1)
		upload.save(destination1)
		#upload.save(destination2)
        
		img_copy = cv2.imread(destination1,1) # will read the uploaded image
		gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY) #convert the coloured uploaded image into a gray image
		face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
		face_recognizer = cv2.face.LBPHFaceRecognizer_create()#builds the recognizer
		face_recognizer.read('recognizer.yml') #loads the yml file that was created earlier. THis file will be used by the recognizer.
		faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5); #detects faces if any, that are present in the uploaded image
		p = len(faces)
		if p == 0:
			kejriwal = "no"
			modi = "no"
			presence_of_face = "no"			
		else:
			presence_of_face = "yes"
			kejriwal = "no"
			modi = "no"
			for(x,y,w,h) in faces:
				
				cv2.rectangle(img_copy,(x,y),(x+w,y+h),(0,255,0),2)
				label_text,conf= face_recognizer.predict(gray[y:y+h,x:x+w])
				#print(label_text)
				#options[label_text]()
				if label_text == 1:
					#global kejriwal
					kejriwal = "yes"
				if label_text == 2:
					#global modi
					modi = "yes"
				if label_text == 3:
					pass

				cv2.rectangle(img_copy, (x,y), (x+w, y+h), (0,255,0), 2)
				cv2.imwrite(destination1,img_copy)
		#print(kejriwal)
		#print(modi)
		#print(presence_of_face)
	return render_template("complete_display_image.html", image_name=filename, value1=presence_of_face, value2=kejriwal, value3=modi)

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("edited_images", filename)
    #return send_from_directory("images", filename)

if __name__ == "__main__":
    app.run(port=4556, debug=True)