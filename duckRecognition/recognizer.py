#!/usr/bin/env python3
# Requires PyAudio and PySpeech.

# Miscellaneous
import sys
sys.path.append('../Identification')
sys.path.append('../audioRecorder')
from os import system
import time
from datetime import datetime
userSpeech = ""

# Azure
from IdentificationServiceHttpClientHelper import *
from IdentifyFile import *

# Audio Recorder
from recordVoice import *

# Speech to Text
import speech_recognition as sr

# Test to Speech
import pyttsx3

# Audiofile to Text
from audioTranscriber import *

# SMS
from send_sms import sendTrafficTextNotification

# Traffic DB
import pymongo
connection = pymongo.MongoClient('ds119223.mlab.com', 19223)
db = connection["cube-traffic"]
db.authenticate("admin", "admin")

# Defined the DB's Collection for Traffic
traffic = db.traffic
userProfiles = db.users

# Good for getting names but not good for getting profileIds
allUserIds = []
users = []

# Azure Subscription Key
subscriptionKey = 'b51342b216294701b97755a73f959ba4'

duckQueryInit = False

def listen():
	# Gives function access to outside variables
	global userSpeech 
	global duckQueryInit

	conversationInit = False
	# Record Audio
	r = sr.Recognizer()
	if not duckQueryInit:
		with sr.Microphone() as source:
			print("Listening...")
			audio = r.listen(source)

	# Speech recognition using Google Speech Recognition
	try:
		# for testing purposes, we're just using the default API key
		# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
		# instead of `r.recognize_google(audio)`
		if not duckQueryInit:
			print("You said: " + r.recognize_google(audio))
			userSpeech = r.recognize_google(audio)

			if "Goodbye Duck" in userSpeech:
				system('say Goodybye human')
			elif "Bye Duck" in userSpeech:
				system('say Goodybye human')
			elif "Shut up duck" in userSpeech:
				system("Well that's rude")

			if "Hey Duck" in userSpeech:
				duckQueryInit = True
				system('say Hello, are you entering or leaving')
			elif "hey duck" in userSpeech:
				duckQueryInit = True
				system('say Hello, are you entering or leaving')
			elif "Hey Doug" in userSpeech:
				duckQueryInit = True
				system('say Hello, are you entering or leaving')
			elif "hey doug" in userSpeech:
				duckQueryInit = True
				system('say Hello, are you entering or leaving')

		# Look for a audio file to text converter, you send the audio file to a funciton and it outputs text
		
		while duckQueryInit:

			now = datetime.now()

			# Converts standard time, so that it's not in military time and defines whether it's AM or PM
			if now.hour >= 13:
				hour = str(now.hour - 12)
				meridiem = "PM"
			elif now.hour == 0:
				hour = str(now.hour + 1)
				meridiem = "AM"
			else:
				hour = str(now.hou)
				meridiem = "AM"

			date = str(datetime.now().strftime('%m-%d-%Y'))

			minute = str(now.minute)

			clockTime = hour + ":" + minute + " " + meridiem

			print("Recording Audio...")
			recordVoice()
			print("Done Recording!")
			newFilePath = '/Users/txt-19/Desktop/duckAi-py/duckRecognition/RECORDING1.wav'
			print(newFilePath)
			audioTranscripter(newFilePath)
			
			logSmsTime = "on " + date + " at " + clockTime
			

			for user in userProfiles.find():
				userIds = user['profileId']
				allUserIds.append(userIds)
			# for user in userProfiles.find():
			# 	user.append('allUserIds')



			# Handles cases when the user says they're entering	
			if "I'm entering" in str(audioTranscripter.speechRecognized):

				identify_file(subscriptionKey, newFilePath, True, allUserIds)

				# Based on the ID returned it assigns that ID to a specific person
				for user in userProfiles.find({'profileId':identify_file.identifiedSpeakerId}):
					identifiedSpeaker = user['fullName']
					print("Identified Speaker = " + identifiedSpeaker)

				for user in userProfiles.find({'profileId':identify_file.identifiedSpeakerId}):
					parentPhoneNumber = user['parentPhoneNumber']
					print("parentPhoneNumber = " + parentPhoneNumber)

				# Says welcome to the Identified Speaker
				system("say Welcome" + identifiedSpeaker)
				sendTrafficTextNotification(identifiedSpeaker + " came into the cube " + logSmsTime, parentPhoneNumber)

				userData = {
					"fullName":identifiedSpeaker,
					"profileId":identify_file.identifiedSpeakerId,
					"trafficQuery":"Entered",
					"date": date,
					"time": clockTime
				}
				db.traffic.insert(userData)
				duckQueryInit = False

			# Handles cases when the user says they're leaving	
			elif "I'm leaving" in str(audioTranscripter.speechRecognized):
				
				identify_file(subscriptionKey, newFilePath, True, allUserIds)

				# Based on the ID returned it assigns that ID to a specific person
				for user in userProfiles.find({'profileId':identify_file.identifiedSpeakerId}):
					identifiedSpeaker = user['fullName']
					print("Identified Speaker = " + identifiedSpeaker)

				# Says good bye to the Identified Speaker
				system("say Goodbye "+identifiedSpeaker)
				sendTrafficTextNotification(identifiedSpeaker + " left the cube " + logSmsTime)

				userData = {
					"fullName":identifiedSpeaker,
					"profileId":identify_file.identifiedSpeakerId,
					"trafficQuery":"Left",
					"date": date,
					"time": clockTime
				}
				db.traffic.insert(userData)
				duckQueryInit = False


	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))

starttime=time.time()

while True:
	listen()
	print("duckQueryInit = " + str(duckQueryInit))
	print ("tick")
	time.sleep(1.0 - ((time.time() - starttime) % 1.0))