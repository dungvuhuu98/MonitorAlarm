#######################################################################################################
# APM Monitor to SPEAKER
# Author: GiangNT
# Release Date: 12/09/2018

# pip install pyttsx3
# pip install pypiwin32
# pip install requests
# pip install colorama
# pip install playsound
# https://github.com/Paradoxis/Windows-Sound-Manager
#######################################################################################################

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
from sound import Sound

#######################################################################################################

APM_API = 'https://apm-new.vndirect.com.vn/AppManager/json/ListAlarms?apikey=30898cfdd40b1930655f329f74c337c8&type=%27critical,warning%27&topN=50' 
WAIT = 10
RATE = 120
LOG_DIR = 'log'
ALARM_CLOCK = False
REMINDER = False
ONE_TIME_PER_MINUTE = False
APP_NAME="APM AI SPEAKER Version 5.9! Copyright \u00a9 2018 by IT VNDIRECT"
TRADING_HOURS = [9, 10, 11, 13, 14]
DEFAULT_VOLUME = 25
VOLUME_1 = 30
VOLUME_2 = 50

duration = 100 # millisecond
freq = 900  # Hz

#######################################################################################################

def banner():
	# Clears the terminal screen, and displays a banner
	os.system('cls')              	
	print(Style.BRIGHT)
	print('     ___________________________')
	print('    /                           /\\')
	print('   /      APM AI SPEAKER      _/ /\\')
	print('  /        Intel 8080        / \/')
	print(' /         Assembler         /\\')
	print('/___________________________/ /')
	print('\___________________________\/')
	print(' \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\')
	print('\nPowered by ' + Fore.BLUE + 'Py' + Fore.YELLOW + 'thon3' + Fore.CYAN)
	
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

def replace_string_in_file(filename, old, new):
	with open(filename) as fr:
		newText=fr.read().replace(old, new)
 
	with open(filename, "w") as fw:
		fw.write(newText)	
	
# https://docs.quantifiedcode.com/python-anti-patterns/maintainability/not_using_with_to_open_files.html	
def read_lines(filename):
	with open(filename,mode="r") as f:
		# Python still executes f.close() even though an exception occurs
		for line in f:
			yield line.strip()

#######################################################################################################

try:
	Sound.volume_set(DEFAULT_VOLUME)
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

	APP_NAME = APP_NAME.replace('\u00a9','')
	say(APP_NAME)
	print (f"{Style.BRIGHT}{Back.GREEN}{Fore.WHITE}", datetime.datetime.now().strftime("%H:%M:%S"), "INFO:", f"{Style.BRIGHT}{Back.MAGENTA}{Fore.WHITE}","Please note the voice and the font color of the alarm. The male voice gives a critical alarm, the female voice for a warning alarm!", f"{Style.RESET_ALL}")
	print()
	say("Please note the voice and the font color of the alarm. The male voice gives a critical alarm, the female voice for a warning alarm")

	print (f"{Style.BRIGHT}{Back.GREEN}{Fore.WHITE}", datetime.datetime.now().strftime("%H:%M:%S"), "INFO:", f"{Style.BRIGHT}{Back.BLUE}{Fore.WHITE}","If there is a critical Alarm during market trading hours, It will speak again every 5 minutes if no one handles it.", f"{Style.RESET_ALL}")
	print()
	say("If there is a critical Alarm during market trading hours, It will speak again every 5 minutes if no one handles it")
	# Beep Alert
	# print (chr(7))
	# print ("\a")
	playsound.playsound('Japanes-bell.wav', True)
except Exception as e:
	print (e)

#######################################################################################################
	
while True:		
	try:
		MINUTE = datetime.datetime.now().minute
		HOUR = datetime.datetime.now().hour
		SECOND = datetime.datetime.now().second
				
		if MINUTE == 0 and ALARM_CLOCK is False:
			# Sound.volume_max()
			Sound.volume_set(VOLUME_2)
			ALARM_MESSAGE = "What time is it now? It's " + time.strftime("%I %p")
			print (f"{Style.BRIGHT}{Back.MAGENTA}{Fore.WHITE}", ALARM_MESSAGE, f"{Style.RESET_ALL}")
			print()
			say(ALARM_MESSAGE)
			Sound.volume_set(VOLUME_1)
			playsound.playsound('big_ben_tune.mp3', True)		

			if HOUR == 8:	
				# Sound.volume_max()
				Sound.volume_set(VOLUME_2)
				playsound.playsound('trong_truong.mp3', True)
				time.sleep(WAIT)
				playsound.playsound('cham_cong_1.mp3', True)
				time.sleep(WAIT)
				playsound.playsound('cham_cong_2.mp3', True)
				time.sleep(WAIT)
				playsound.playsound('cham_cong_1.mp3', True)
				Sound.volume_set(DEFAULT_VOLUME)						
			elif HOUR == 9:
				Sound.volume_set(VOLUME_2)
				print (f"{Style.BRIGHT}{Back.MAGENTA}{Fore.WHITE}", "Hey, IT guys! Please focus on monitoring! It's now the market open time. Enjoy your trading system and Have a safe flight!", f"{Style.RESET_ALL}")
				print()
				say("Hey, IT guys! Please focus on monitoring! It's now the market open time. Enjoy your trading system and Have a safe flight!")				
			elif HOUR == 12:				
				Sound.volume_set(VOLUME_2)
				print (f"{Style.BRIGHT}{Back.MAGENTA}{Fore.WHITE}", "It's now the break time. Wish you a delicious lunch meal!", f"{Style.RESET_ALL}")
				print()
				say("It's now the break time. Wish you a delicious lunch meal!")				
			elif HOUR == 13:				
				Sound.volume_set(VOLUME_2)
				print (f"{Style.BRIGHT}{Back.MAGENTA}{Fore.WHITE}", "Wake up, IT guys! It's now the market open again. Please don't make any mistake! Come on, you can do it.", f"{Style.RESET_ALL}")
				print()
				say("Wake up, IT guys! It's now the market open again. Please don't make any mistake! Come on, you can do it.")				
			elif HOUR == 15:				
				Sound.volume_set(VOLUME_2)
				print (f"{Style.BRIGHT}{Back.MAGENTA}{Fore.WHITE}", "Well done IT guys! It's now the market closed time. Congratulations to you, today your trading system has no serious problems.", f"{Style.RESET_ALL}")
				print()			
				say("Well done IT guys! It's now the market closed time. Congratulations to you, today your trading system has no serious problems.")
												
			Sound.volume_set(DEFAULT_VOLUME)			
			ALARM_CLOCK = True
			time.sleep(WAIT)
			
		elif MINUTE != 0:
			ALARM_CLOCK = False		

		if MINUTE == 30 and REMINDER is False:	
			if HOUR == 8:	
				# Sound.volume_max()
				Sound.volume_set(VOLUME_2)
				playsound.playsound('trong_truong.mp3', True)
				time.sleep(WAIT)
				playsound.playsound('cham_cong_1.mp3', True)
				time.sleep(WAIT)
				playsound.playsound('cham_cong_2.mp3', True)
				time.sleep(WAIT)
				playsound.playsound('cham_cong_3.mp3', True)
				Sound.volume_set(DEFAULT_VOLUME)
			if HOUR == 11:	
				# Sound.volume_max()
				Sound.volume_set(VOLUME_2)	
				print (f"{Style.BRIGHT}{Back.MAGENTA}{Fore.WHITE}", "Good job IT guys, It's now the market break time. Enjoy your lunch!", f"{Style.RESET_ALL}")
				print()
				say("Good job IT guys, It's now the market break time. Enjoy your lunch!")
				Sound.volume_set(DEFAULT_VOLUME)
			###if HOUR == 15:	
				# Sound.volume_max()
				###Sound.volume_set(VOLUME_2)
				###playsound.playsound('trong_truong.mp3', True)
				###time.sleep(WAIT)
				###print (f"{Style.BRIGHT}{Back.MAGENTA}{Fore.WHITE}", "And Now Its time to relax. Please go out and Enjoy your plank and breath!", f"{Style.RESET_ALL}")
				###print()				
				###say("And Now Its time to relax. Please go out and Enjoy your plank and breath!")								
				###Sound.volume_set(DEFAULT_VOLUME)				
			if HOUR == 17:
				# Sound.volume_max()
				Sound.volume_set(VOLUME_2)
				playsound.playsound('trong_truong.mp3', True)
				time.sleep(WAIT)
				playsound.playsound('cham_cong_1.mp3', True)
				time.sleep(WAIT)
				playsound.playsound('cham_cong_2.mp3', True)
				time.sleep(WAIT)
				playsound.playsound('cham_cong_1.mp3', True)
				Sound.volume_set(DEFAULT_VOLUME)
				
			REMINDER = True
		elif MINUTE != 30:
			REMINDER = False				
		
		LOG_FILE = LOG_DIR + "\log-" + str(date.today()) + ".txt"
		LOG_CRITICAL = LOG_DIR + "\log-critical-" + str(date.today()) + ".txt"
		
		if os.path.isfile(LOG_FILE) is False:
			Path(LOG_FILE).touch() # Create a emty file if not exist
			
		if os.path.isfile(LOG_CRITICAL) is False:
			Path(LOG_CRITICAL).touch() # Create a emty file if not exist			
	
		r = requests.get(APM_API)
		data = r.json()

		lines = list(read_lines(LOG_FILE))
		# print(lines)
		
		lines_critical = list(read_lines(LOG_CRITICAL))
		# print(lines_critical)
		
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
			# Alert again if STATUS is critical in Trading hours	
			if element['MODTIME'] in lines_critical and MINUTE%5 == 0 and ONE_TIME_PER_MINUTE is False:	
				# List Index Out of Range in Windows Server 2008 R2			
				engine.setProperty('voice', voices[0].id)
				
				MESSAGE = element['MESSAGE'].replace('<br>2.','')
				MESSAGE = MESSAGE.replace('<br>1.','')
				MESSAGE = MESSAGE.replace('<br>','')
				MESSAGE = MESSAGE.replace('<ol>','')
				MESSAGE = MESSAGE.replace('</ol>','')
				MESSAGE = MESSAGE.replace('<li>','')
				MESSAGE = MESSAGE.replace('</li>','')
				# Trim all space and tab in MESSAGE
				MESSAGE = ' '.join(MESSAGE.split())				

				print (f"{Style.BRIGHT}{Back.GREEN}{Fore.WHITE}", element['FORMATTEDDATE'], f"{Back.WHITE}{Fore.MAGENTA}", "It's now", datetime.datetime.now().strftime("%H:%M"), f"{Fore.BLUE}", "This is a reminder. Who handles this?", f"{Back.RED}{Fore.YELLOW}", MESSAGE, f"{Style.RESET_ALL}" )								
				# Prints a newline
				print() 
				# Cut string "Health of ... <br>Root Cause : ...<br>"
				MESSAGE = element['MESSAGE'].split('<br>')[0]					
				MESSAGE = ' '.join(MESSAGE.split())					
				say("This is a reminder. Who handles this? " + MESSAGE)	
				ONE_TIME_PER_MINUTE = True
			elif MINUTE%5 != 0:
				ONE_TIME_PER_MINUTE = False
				
			if element['MODTIME'] not in lines:
				if element['STATUS'] == 'critical':
					# List Index Out of Range in Windows Server 2008 R2
					engine.setProperty('voice', voices[0].id)
					FG = Fore.YELLOW
					BG = Back.RED
				else:
					# List Index Out of Range in Windows Server 2008 R2
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
								
				CRITICAL_IN_TRADING_HOURS = True
				
				if element['STATUS'] == 'critical' and HOUR not in TRADING_HOURS:
					CRITICAL_IN_TRADING_HOURS = False															
				
				if element['STATUS'] == 'warning':
					CRITICAL_IN_TRADING_HOURS = False					
						
				with open(LOG_FILE,mode="a") as fa:
					fa.write(element['MODTIME'] + '\n')	
				
				if CRITICAL_IN_TRADING_HOURS is True:
					with open(LOG_CRITICAL,mode="a") as fa:
						fa.write(element['MODTIME'] + '\n')							

		# print("INFO: " + time.strftime("%c"))
		time.sleep(WAIT) # delays for X seconds
		# print("INFO: " + time.strftime("%c"))					
	except Exception as e:
		print (e)