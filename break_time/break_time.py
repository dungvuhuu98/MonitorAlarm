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
WAIT = 2

# defining the api-endpoint  
# API_ENDPOINT = "http://localhost:5000/api"
API_ENDPOINT = "https://speaker.vndirect.com.vn/api"

headers = {
	'content-type': 'application/json',
	'x-api-key': '51e2ac2ebd8z9d112af03eb0c82'
}


def break_time_noti():
	try:
		# Sound.volume_max()
		Sound.volume_set(VOLUME_MAX)
		playsound.playsound('trong_truong.mp3', True)
		time.sleep(WAIT)
		# data to be sent to api 
		payload = {"message": "Đia anh chị em khối Công nghệ", "language":"vn"}
		# sending post request and saving response as response object 
		requests.post(API_ENDPOINT, data = json.dumps(payload), headers=headers)
		time.sleep(WAIT)
		payload = {"message": "Với sức trẻ, khỏe và sự đồng lòng của chúng ta, cộng với sự mạnh mẽ tuổi 15 của VND, chúng ta cùng nỗ lực và hoàn thành tốt các mục tiêu nhé.", "language":"vn"}
		requests.post(API_ENDPOINT, data = json.dumps(payload), headers=headers)
		time.sleep(WAIT)
		payload = {"message": "Để giúp anh chị em có thời gian thư giãn, tập thể dục, khôi phục sức khỏe, chúng tôi xin đề xuất triển khai Bờ rếch tham hàng ngày.", "language":"vn"}
		requests.post(API_ENDPOINT, data = json.dumps(payload), headers=headers)
		time.sleep(WAIT)
		payload = {"message": "Chúng ta sẽ được nhắc nhở nghỉ ngơi lúc 15 giờ 30 phút và nhắc quay trở lại làm việc lúc 15 giờ 45 phút bắt đầu từ hôm nay ngày 1 tháng 6 năm 2021", "language":"vn"}
		requests.post(API_ENDPOINT, data = json.dumps(payload), headers=headers)
		time.sleep(WAIT)
		payload = {"message": "Anh chị em có ý tưởng cho hoạt động chung vào giờ này, hay muốn mở nhạc thể loại gì thì đưa ý kiến đề xuất trong G giúp Đường bột nhé.", "language":"vn"}
		requests.post(API_ENDPOINT, data = json.dumps(payload), headers=headers)
		time.sleep(WAIT)
		payload = {"message": "Chúc anh chị em có thời gian ri lách hiệu quả.", "language":"vn"}
		requests.post(API_ENDPOINT, data = json.dumps(payload), headers=headers)
	except:
		traceback.print_exc()


break_time_noti()
