# Author: GiangNT
# Date: 21/09/2019

# https://www.rabbitmq.com/tutorials/tutorial-one-python.html
# pip install pika
# pip install pyttsx3
# pip install colorama

# https://pypi.org/project/cowsay/
# pip install cowsay

import pika
import pyttsx3
import ctypes
import colorama
from colorama import Fore, Back, Style
import datetime
import cowsay

RATE = 120
APP_NAME = "Speaker API Version 1.0!"

def say(text):
	engine.say(text)
	engine.runAndWait()

def callback(ch, method, properties, body):	
	# How to convert bytes type to string type
	message = body.decode("utf-8") 
	print (f"{Style.BRIGHT}{Back.GREEN}{Fore.WHITE}", datetime.datetime.now().strftime("%H:%M:%S"), "INFO:", f"{Style.BRIGHT}{Back.MAGENTA}{Fore.WHITE}",message, f"{Style.RESET_ALL}")
	print()
	say(message)

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
	channel.queue_declare(queue='speaker')

	channel.basic_consume(queue='speaker', on_message_callback=callback, auto_ack=True)

	cowsay.tux(APP_NAME)
	say(APP_NAME)
	
	channel.start_consuming()

except Exception as e:
	print (e)