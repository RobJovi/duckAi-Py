#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
import sys
sys.path.append('../Identification')
sys.path.append('../audioRecorder')
from os import system
from recordVoice import *
from IdentifyFile import *
#import pyttsx
import speech_recognition as sr
import time
import pyttsx3



userSpeech = ""


duckQueryInit = False



def listen():
	# Gives function access to outside variables
	global userSpeech 
	global duckQueryInit

	conversationInit = False
	# Record Audio
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Listening...")
		audio = r.listen(source)

	# Speech recognition using Google Speech Recognition
	try:
		# for testing purposes, we're just using the default API key
		# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
		# instead of `r.recognize_google(audio)`
		print("You said: " + r.recognize_google(audio))
		userSpeech = r.recognize_google(audio)

		if "Hey Duck" in userSpeech:
			duckQueryInit = True
			system('say Hello, are you entering or leaving')

		# Look for a audio file to text converter, you send the audio file to a funciton and it outputs text
		if duckQueryInit:
			while duckQueryInit:
				recordVoice()
				if "I'm entering" in userSpeech:
					system("say Okay your entering")
					duckQueryInit = False
				elif "I'm leaving" in userSpeech:
					system("say Okay your leaving")
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