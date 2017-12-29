import requests
import time
import shutil
from settings import TUMBLR_API_KEY

LOOP = 10
URL = 'https://api.tumblr.com/v2/tagged'
payload = {
    'api_key': TUMBLR_API_KEY,
    'tag': '北村一輝'
}
#悪人代表: 北野武, 遠藤憲一, 寺島進, 的場浩司, 國村隼, 島田紳助, 小沢一郎, 香川照之, 吉田鋼太郎, 小家健太, 山田孝之, 藤原竜也, 北村一輝
# 善人代表: 神木隆之介、綾野剛, 斎藤工、佐藤健、要潤
image_idx = 0

photo_urls = []
for i in range(LOOP):
    response_json = requests.get(URL, params=payload).json()
    for data in response_json['response']:
        if data['type'] != 'photo':
            continue
        for photo in data['photos']:
            photo_urls.append(photo['original_size']['url'])
    if(len(response_json['response']) == 0):
        continue
    payload['before'] = response_json['response'][(len(response_json['response']) - 1)]['timestamp']

for photo_url in photo_urls:
    path = "datasets/badman/" + 'kitamura' + str(image_idx) + ".png"
    r = requests.get(photo_url, stream=True)
    if r.status_code == 200:
      with open(path, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
      image_idx+=1
