# APM Monitor to SPEAKER
# Author: GiangNT
# Release Date: 12/07/2018

# pip install pyttsx3
# pip install pypiwin32
# pip install requests
# pip install colorama
# pip install playsound

import os.path
import os
import json
import time
import requests
from datetime import date
from pathlib import Path
import pyttsx3
import colorama
from colorama import Fore, Back, Style
import playsound
import datetime
import winsound
import ctypes

APM_API = 'https://apm.vndirect.com.vn/AppManager/json/ListAlarms?apikey=51e2ac2ebd89d112af03eb0c51d538d5&type=%27critical,warning%27&topN=50' 
WAIT = 10
RATE = 120
LOG_DIR = 'log'
ALARM_CLOCK = False
APP_NAME="APM SPEAKER version 1.0! Copyright \u00a9 2018 by IT VNDIRECT"

duration = 100 # millisecond
freq = 1000  # Hz

def display_title_bar():
	# Clears the terminal screen, and displays a title bar.
	os.system('cls')              	
	print(f"{Style.BRIGHT}{Fore.YELLOW}")
	for CHAR in APP_NAME:
		# sleep(0.1)	
		winsound.Beep(freq, duration)	
		# In Python 3.x, the end=' ' part will place a space after the displayed string instead of a newline
		print(CHAR, end=' ', flush=True)
	print (f"{Style.RESET_ALL}")
	print()
	
	
def say(text):
    engine.say(text)
    engine.runAndWait()
 
def read_lines(filename):
	with open(filename,mode="r") as f:
		for line in f:
			yield line.strip()

ctypes.windll.kernel32.SetConsoleTitleW(APP_NAME)
display_title_bar()
			
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

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
say(APP_NAME)
say("Please note that the voice and the font color of alarm. The male voice gives a critical alarm, the female voice for a warning alarm")
# Beep Alert
# print (chr(7))
# print ("\a")
playsound.playsound('Japanes-bell.wav', True)
					
while True:		
	minute = datetime.datetime.now().minute
	hour = datetime.datetime.now().hour
	if minute == 0 and ALARM_CLOCK is False:
		ALARM_MESSAGE = "IT IS NOW " + str(hour) + " O'CLOCK"
		print (f"{Style.BRIGHT}{Fore.CYAN}", ALARM_MESSAGE, f"{Style.RESET_ALL}")
		say(ALARM_MESSAGE)
		playsound.playsound('big_ben_tune.mp3', True)		
		ALARM_CLOCK = True
		time.sleep(WAIT)
	elif minute != 0:
		ALARM_CLOCK = False
	
	filename = LOG_DIR + "\log-" + str(date.today()) + ".txt"
	if os.path.isfile(filename) is False:
		Path(filename).touch() # Create a emty file if not exist

	try:
		r = requests.get(APM_API)
		data = r.json()

		lines = list(read_lines(filename))
		# print(lines)

		with open(filename,mode="a") as fw:
			response = data['response']['result']
			# Reverse a list Alarms
			response = response[::-1]
			for element in response:			
				# if No Alarms available
				if 'Message' in element and element['Message'] == "No Alarms available.":
					# print (f"{Style.BRIGHT}{Back.BLUE}{Fore.WHITE}No Alarms available.{Style.RESET_ALL}" )
					break
				# Ignore Monitor Group
				if element['TYPEDISPLAYNAME'] == 'Monitor Group':
					continue
				if element['MODTIME'] not in lines:										
					if element['STATUS'] == 'critical':
						engine.setProperty('voice', voices[0].id)
						FG = Fore.YELLOW
						BG = Back.RED
					else:
						engine.setProperty('voice', voices[1].id)
						FG = Fore.BLUE					
						BG = Back.WHITE
					MESSAGE = element['MESSAGE'].replace('<br>2.','')
					MESSAGE = MESSAGE.replace('<br>1.','')
					MESSAGE = MESSAGE.replace('<br>','')
					MESSAGE = MESSAGE.replace('<ol>','')
					MESSAGE = MESSAGE.replace('</ol>','')
					MESSAGE = MESSAGE.replace('<li>','')
					MESSAGE = MESSAGE.replace('</li>','')
					# Trim all space and tab in MESSAGE
					MESSAGE = ' '.join(MESSAGE.split())					
					print (f"{Style.BRIGHT}{Back.GREEN}{Fore.WHITE}", element['FORMATTEDDATE'], f":{Style.RESET_ALL}{Style.BRIGHT}{BG}{FG}", MESSAGE, f"{Style.RESET_ALL}" )
					# Prints a newline
					print() 
					# Cut string "Health of ... <br>Root Cause : ...<br>"
					MESSAGE = element['MESSAGE'].split('<br>')[0]					
					MESSAGE = ' '.join(MESSAGE.split())					
					say(MESSAGE)
					fw.write(element['MODTIME'] + '\n')	
					
	except Exception as e:
		print (e)

	# print("INFO: " + time.strftime("%c"))
	time.sleep(WAIT) # delays for X seconds
	# print("INFO: " + time.strftime("%c"))