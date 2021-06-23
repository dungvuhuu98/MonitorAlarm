# Lunch Break Time Noti
# Author: GiangNT
# Date: 12/12/2019

# curl -i -X POST -H 'Content-Type: application/json' -H 'x-api-key: 51e2ac2ebd8z9d112af03eb0c82' -d '{"message": "Documentation is like sex. When it is good, it is very, very good and when it is bad, it is better than nothing", "language":"en"}' https://speaker.vndirect.com.vn/api

# curl -i -X POST -H 'Content-Type: application/json' -H 'x-api-key: 51e2ac2ebd8z9d112af03eb0c82' -d '{"message": "Cong hoa xa hoi chu nghia viet nam", "language":"vn"}' https://speaker.vndirect.com.vn/api

# pip install requests
# pip install playsound
# https://github.com/Paradoxis/Windows-Sound-Manager

import time
import json
import requests
import traceback
import playsound
from sound import Sound

VOLUME_MAX = 100
WAIT = 5

# defining the api-endpoint  
# API_ENDPOINT = "http://localhost:5000/api"
API_ENDPOINT = "https://speaker.vndirect.com.vn/api"

headers = {
	'content-type': 'application/json',
	'x-api-key': '51e2ac2ebd8z9d112af03eb0c82'
}


def lunch_break_time_noti():
	try:
		# Sound.volume_max()
		Sound.volume_set(VOLUME_MAX)
		playsound.playsound('trong_truong.mp3', True)
		time.sleep(WAIT)
		# data to be sent to api 
		payload = {"message": "Hiện đã hết giờ ngủ trưa", "language":"vn"}
		# sending post request and saving response as response object 
		requests.post(API_ENDPOINT, data = json.dumps(payload), headers=headers)
		time.sleep(WAIT)
		payload = {"message": "Mời anh em bật đèn điện và trở lại công việc", "language":"vn"}
		requests.post(API_ENDPOINT, data = json.dumps(payload), headers=headers)
		time.sleep(WAIT)
		payload = {"message": "Chúc mọi người làm việc hiệu quả", "language":"vn"}
		requests.post(API_ENDPOINT, data = json.dumps(payload), headers=headers)

	except:
		traceback.print_exc()


lunch_break_time_noti()
