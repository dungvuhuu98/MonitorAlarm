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
APP_NAME="APM SPEAKER Version 2.0! Copyright \u00a9 2018, by IT VNDIRECT"

duration = 100 # millisecond
freq = 900  # Hz

def banner():
	# Clears the terminal screen, and displays a banner
	os.system('cls')              	
	print(Style.BRIGHT)
	print('     ___________________________')
	print('    /                           /\\')
	print('   /       APM SPEAKER        _/ /\\')
	print('  /        Intel 8080        / \/')
	print(' /         Assembler         /\\')
	print('/___________________________/ /')
	print('\___________________________\/')
	print(' \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\')
	print('\nPowered by ' + Fore.BLUE + 'Py' + Fore.YELLOW + 'thon' + Fore.CYAN)
	
	for CHAR in APP_NAME:
		# sleep(0.1)	
		winsound.Beep(freq, duration)	
		# In Python 3.x, the end=' ' part will place a space after the displayed string instead of a newline
		print(CHAR, end=' ', flush=True)
	print (Style.RESET_ALL)
	print()
	
	
def say(text):
    engine.say(text)
    engine.runAndWait()

# https://docs.quantifiedcode.com/python-anti-patterns/maintainability/not_using_with_to_open_files.html	
def read_lines(filename):
	with open(filename,mode="r") as f:
		# Python still executes f.close() even though an exception occurs
		for line in f:
			yield line.strip()

ctypes.windll.kernel32.SetConsoleTitleW(APP_NAME)
banner()
			
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

# APP_NAME = APP_NAME.replace('\u00a9','')
say("APM SPEAKER for IT VNDIRECT")
say("Please note the voice and the font color of the alarm. The male voice gives a critical alarm, the female voice for a warning alarm")
# Beep Alert
# print (chr(7))
# print ("\a")
playsound.playsound('Japanes-bell.wav', True)
					
while True:		
	try:
		minute = datetime.datetime.now().minute
		
		if minute == 0 and ALARM_CLOCK is False:
			ALARM_MESSAGE = "What time is it now? It's " + time.strftime("%I %p")
			print (f"{Style.BRIGHT}{Back.MAGENTA}{Fore.WHITE}", ALARM_MESSAGE, f"{Style.RESET_ALL}")
			print()
			say(ALARM_MESSAGE)
			playsound.playsound('big_ben_tune.mp3', True)		
			ALARM_CLOCK = True
			time.sleep(WAIT)
		elif minute != 0:
			ALARM_CLOCK = False
	
		LOG_FILE = LOG_DIR + "\log-" + str(date.today()) + ".txt"
		if os.path.isfile(LOG_FILE) is False:
			Path(LOG_FILE).touch() # Create a emty file if not exist
	
		r = requests.get(APM_API)
		data = r.json()

		lines = list(read_lines(LOG_FILE))
		# print(lines)
		
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
				print (f"{Style.BRIGHT}{Back.GREEN}{Fore.WHITE}", element['FORMATTEDDATE'], f"{Style.RESET_ALL}{Style.BRIGHT}{BG}{FG}", MESSAGE, f"{Style.RESET_ALL}" )
				# Prints a newline
				print() 
				# Cut string "Health of ... <br>Root Cause : ...<br>"
				MESSAGE = element['MESSAGE'].split('<br>')[0]					
				MESSAGE = ' '.join(MESSAGE.split())					
				say(MESSAGE)
				# Alert again if STATUS is critical in Trading hours
				hour = datetime.datetime.now().hour
				# print (hour)
				LOG = False
				
				if element['STATUS'] == 'critical' and hour < 9:
					LOG = True
								
				if element['STATUS'] == 'critical' and hour > 14:
					LOG = True					
				
				if element['STATUS'] == 'warning':
					LOG = True					
						
				if LOG is True:
					with open(LOG_FILE,mode="a") as fw:
						fw.write(element['MODTIME'] + '\n')	

		# print("INFO: " + time.strftime("%c"))
		time.sleep(WAIT) # delays for X seconds
		# print("INFO: " + time.strftime("%c"))					
	except Exception as e:
		print (e)