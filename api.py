import audioAnalysis as adA
# adA.speakerDiarizationWrapper("dataFiles/mc1.wav",0,False)
import speech_recognition as sr
from textblob import TextBlob
from flask import Flask, request
from flask_restful import Resource, Api
import base64
app = Flask(__name__)
api = Api(app)

r = sr.Recognizer()


class SpeechProcess(Resource):
	# @jwt_required()
	def post(self):

		req_data = request.get_json()
		fileStr = req_data["imageData"]
		fileStr = (str.encode(fileStr))
		print(fileStr)

		with open("output/inputAudio.wav", "wb") as fh:
			fh.write(base64.decodebytes(fileStr))

		filePath = "output/inputAudio.wav"
		adA.speakerDiarizationWrapper(filePath,0,False)

		with open("output/outImg.jpg", "rb") as image_file:
			img_data = base64.b64encode(image_file.read())


		harvard = sr.AudioFile(filePath)
		outJson = {}
		with harvard as source:
			audio = r.record(source)

			txt = r.recognize_google(audio)

			if(len(list(txt)) > 0):
				print(txt)
				sentiment = TextBlob(txt)
				img_data = img_data.decode("utf-8")
				outJson = {
					"orignalText" : txt,
					"Score": sentiment.sentiment.polarity,
					"imgData": img_data
				}

			else:
				outJson = {
					"Score: ": "Empty text"
				}


		return (outJson)

	def get(self):
		return ({"data":"information"})

api.add_resource(SpeechProcess,"/getData")

app.run(host= "127.0.0.1", port = "2935", debug = True)
