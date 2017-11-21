#!/usr/bin/env python3
# Requires PyAudio and PySpeech.

# Miscellaneous
import sys
sys.path.append('../Identification')
sys.path.append('../audioRecorder')
from os import system
import time
from datetime import datetime
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
# Make it send a text message of the log, so Oscar is at the cube at (time of arrival)

userSpeech = ""

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

			if "Hey Duck" in userSpeech:
				duckQueryInit = True
				system('say Hello, are you entering or leaving')

		# Look for a audio file to text converter, you send the audio file to a funciton and it outputs text
		
		while duckQueryInit:
			print("Recording Audio...")
			recordVoice()
			print("Done Recording!")
			newFilePath = '/Users/txt-19/Desktop/duckAi-py/duckRecognition/RECORDING1.wav'
			print(newFilePath)
			audioTranscripter(newFilePath)
			
			currentTime = "on " + str(datetime.now().strftime('%m-%d-%Y')) + " at " + str(datetime.now().strftime('%H:%M'))
			allUserIds = ['a8363fca-7bc4-4b7b-b4da-673eacedc05d', '2e113a5a-161c-4cad-af96-c3e7b200adb4','53115c36-9984-460d-b944-246a59dbe071', '63f680c0-85c4-47d5-97b6-d4c4d4aa56d8']


			if str(audioTranscripter.speechRecognized) == None:
				system("say Sorry, I didn't get that?")

			# Handles cases when the user says they're entering	
			elif "I'm entering" in str(audioTranscripter.speechRecognized):

				identify_file(subscriptionKey, newFilePath, True, allUserIds)

				# Based on the ID returned it assigns that ID to a specific person
				if identify_file.identifiedSpeakerId == 'a8363fca-7bc4-4b7b-b4da-673eacedc05d':
					identifiedSpeaker = 'Nabil'
				elif identify_file.identifiedSpeakerId == '63f680c0-85c4-47d5-97b6-d4c4d4aa56d8':
					identifiedSpeaker = 'Anthony'
				elif identify_file.identifiedSpeakerId == '2e113a5a-161c-4cad-af96-c3e7b200adb4':
					identifiedSpeaker = 'Robert'
				elif identify_file.identifiedSpeakerId == '53115c36-9984-460d-b944-246a59dbe071':
					identifiedSpeaker = 'Asarel'
				else:
					identifiedSpeaker = None

				# Says welcome to the Identified Speaker
				system("say Welcome" + identifiedSpeaker)
				sendTrafficTextNotification(identifiedSpeaker + " came into the cube " + currentTime)
				duckQueryInit = False

			# Handles cases when the user says they're leaving	
			elif "I'm leaving" in str(audioTranscripter.speechRecognized):
				
				identify_file(subscriptionKey, newFilePath, True, allUserIds)

				# Based on the ID returned it assigns that ID to a specific person
				if identify_file.identifiedSpeakerId == 'a8363fca-7bc4-4b7b-b4da-673eacedc05d':
					identifiedSpeaker = 'Nabil'
				elif identify_file.identifiedSpeakerId == '63f680c0-85c4-47d5-97b6-d4c4d4aa56d8':
					identifiedSpeaker = 'Anthony'
				elif identify_file.identifiedSpeakerId == '2e113a5a-161c-4cad-af96-c3e7b200adb4':
					identifiedSpeaker = 'Robert'
				elif identify_file.identifiedSpeakerId == '53115c36-9984-460d-b944-246a59dbe071':
					identifiedSpeaker = 'Asarel'
				else:
					identifiedSpeaker = None

				# Says good bye to the Identified Speaker
				system("say Goodbye "+identifiedSpeaker)
				sendTrafficTextNotification(identifiedSpeaker + " left the cube " + currentTime)
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