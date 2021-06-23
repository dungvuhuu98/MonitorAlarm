# Author: GiangNT
# Date: 21/09/2019

# https://www.rabbitmq.com/tutorials/tutorial-one-python.html
# pip install pika
# pip install pyttsx3
# pip install colorama

# https://pypi.org/project/cowsay/
# pip install cowsay
# https://github.com/jeffbuttars/cowpy

# https://www.devdungeon.com/content/create-ascii-art-text-banners-python
# pip install pyfiglet

# pip install requests
# pip install playsound
# https://github.com/Paradoxis/Windows-Sound-Manager

# pip install --upgrade google-cloud-texttospeech
# https://cloud.google.com/text-to-speech/docs/reference/libraries#client-libraries-install-python

import pika
import pyttsx3
import ctypes
import colorama
from colorama import Fore, Back, Style
import datetime
import cowsay
from pyfiglet import Figlet
import time
import requests
import playsound
import json
from sound import Sound
from google.cloud import texttospeech
import glob
import os

WAIT = 5
RATE = 120
APP_NAME = "Speaker API Version 1.2! This is a Vietnamese Speaker version"
DEFAULT_VOLUME = 50

# defining the api-endpoint  
API_ENDPOINT = "https://api.fpt.ai/hmi/tts/v5"

headers = {
	'api-key': 'TlE2DQp20JnrM33foXL181iogfE3oaql',
	'speed': '',
	'voice': 'lannhi'
}

def say_vietnamese_fpt_api(message):
	try:
		# data to be sent to api 
		payload = message
		res = requests.request('POST', API_ENDPOINT, data=payload.encode('utf-8'), headers=headers)
		
		# Error handling
		# Check for HTTP codes other than 200
		if res.status_code != 200:
			print('Status:', response.status_code, 'Problem with the request. Exiting.')
			exit(1)

		# Decode the JSON response into a dictionary and use the data
		data = res.json()	
		#print (data)		
		MP3_LINK = data['async']
		#print(MP3_LINK)
		playsound.playsound(MP3_LINK, True)
	except Exception as e:	
		if "A problem occurred in initializing MCI" in str(e):
			#print ("Please wait a moment while creating a mp3 file for the first time!")
			time.sleep(WAIT)			
			playsound.playsound(MP3_LINK, True)
		else:
			print (str(e))

def say_vietnamese_gcp_api(message):
	try:

		# Set environment variables
		os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "integral-surfer-228905-196c50a15464.json"

		# Get environment variables
		#print (os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))

		# Instantiates a client
		client = texttospeech.TextToSpeechClient()

		# Set the text input to be synthesized
		synthesis_input = texttospeech.types.SynthesisInput(text=message)

		# Build the voice request, select the language code ("en-US") and the ssml
		# voice gender ("neutral")
		voice = texttospeech.types.VoiceSelectionParams(
			language_code='vi-VN',
			ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

		# Select the type of audio file you want returned
		audio_config = texttospeech.types.AudioConfig(
			audio_encoding=texttospeech.enums.AudioEncoding.MP3)

		# Perform the text-to-speech request on the text input with the selected
		# voice parameters and audio file type
		response = client.synthesize_speech(synthesis_input, voice, audio_config)

		MP3_FILE = "C:\\temp\\" + datetime.datetime.now().strftime("%d%m%Y_%H%M%S") + ".mp3"
		# The response's audio_content is binary.
		with open(MP3_FILE, 'wb') as out:
			# Write the response to the output file.
			out.write(response.audio_content)
			#print('Audio content written to file "output.mp3"')	

		playsound.playsound(MP3_FILE, True)
		
		#if os.path.exists(MP3_FILE):
		#	os.remove(MP3_FILE)
			
	except Exception as e:	
		print (str(e))
		
def say(message):
	engine.say(message)
	engine.runAndWait()

def callback(ch, method, properties, body):	
	# How to convert bytes type to string type
	message = body.decode("utf-8") 
	print (f"{Style.BRIGHT}{Back.GREEN}{Fore.WHITE}", datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "INFO:", f"{Style.BRIGHT}{Back.WHITE}{Fore.MAGENTA}",message, f"{Style.RESET_ALL}")
	print()
	Sound.volume_set(DEFAULT_VOLUME)
	say_vietnamese_gcp_api(message)

try:	
	ctypes.windll.kernel32.SetConsoleTitleW(APP_NAME)
	colorama.init()
	engine = pyttsx3.init()
	# print (engine.getProperty('rate'))
	# print (engine.getProperty('volume'))
	# print (engine.getProperty('voice'))
	# print (engine.getProperty('voices'))

	# Changing voices
	voices = engine.getProperty('voices')
	# Changing index changes voices but ony 0 and 1 are working here
	# engine.setProperty('voice', voices[1].id) 

	# Changing speech rate
	# engine.setProperty('rate', newVoiceRate)
	# Replace newVoiceRate with rate according to requirement. It's integer speech rate in words per minute. Defaults to 200 word per minute.
	rate = engine.getProperty('rate')
	engine.setProperty('rate', RATE)

	credentials = pika.PlainCredentials('admin', 'vnds@1234')
	parameters = pika.ConnectionParameters('10.200.30.8', 5672,'/',credentials)
	connection = pika.BlockingConnection(parameters)

	channel = connection.channel()
	channel.queue_declare(queue='speaker_vn')

	channel.basic_consume(queue='speaker_vn', on_message_callback=callback, auto_ack=True)

	
	custom_fig = Figlet(font='graffiti')
	#print(custom_fig.renderText('Hello!!'))
	#cowsay.tux(APP_NAME)
	cowsay.turtle(custom_fig.renderText("API"))

	say(APP_NAME)
	print (f"{Style.BRIGHT}{Back.GREEN}{Fore.WHITE}", datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "INFO:", f"{Style.BRIGHT}{Back.MAGENTA}{Fore.WHITE}","Hello IT Guys, I'm Mr Turtle from VNDIRECT. I am very excited now. I'll use Google API to speak in Vietnamese", f"{Style.RESET_ALL}")
	print()
	say("Hello IT Guys, I'm Mr Turtle from VND. I am very excited now. I'll use Google API to speak in Vietnamese")
	#playsound.playsound("bonjour_vietnam.mp3", True)
		
	filelist=glob.glob("C:\\temp\\*.mp3")
	for file in filelist:
		os.remove(file)	
	
	channel.start_consuming()

except Exception as e:
	print (e)