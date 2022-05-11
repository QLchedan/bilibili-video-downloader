from requests import get
from bs4 import BeautifulSoup
from ffmpy3 import FFmpeg
from demjson import decode
from time import time, sleep
from os import system
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
    'Referer': 'http://www.bilibili.com/',
}

def download(name, url):
    r = get(url, stream=True, headers=headers, verify=False)
    print(r)
    length = float(r.headers['content-length'])
    f = open(name, 'wb')
    count = 0
    time1 = time()
    for chunk in r.iter_content(chunk_size = 1024):
        if chunk:
            f.write(chunk)
            count += len(chunk)
            if time() - time1 > 0.25:
                system('cls')
                p = count / length * 100
                print(name + ': ' + str(round(p, 2)) + '%')
                time1 = time()
    f.close()
print('欢迎来到bilibili视频解析下载。此软件不支持对1080p+,1080p60以及4k画质视频的解析。(需要ffmpeg)')
print('by 千里扯淡 2022')
bv_id = input('请输入视频BV号:')
soup = BeautifulSoup(get('https://www.bilibili.com/video/' + bv_id, verify=False).content, 'html.parser')
scripts_list = soup.find_all('script')
info = scripts_list[3].contents[0][20:-1] + '}'
py_obj = decode(info)
quality_list = list()
quality = int()
for i in py_obj['data']['accept_description']:
    if i != '高清 1080P+' and i != '超清 4K' and i != '高清 1080P60':
        quality_list.append(i)
print('请输入将要下载的画质:')
for i in range(len(quality_list)):
    print(str(i) + ' ' + quality_list[i])
quality = int(input())
if quality < 0 or quality > 3:
    print('错误,请检查输入')
    exit()
print('视频下载开始')
sleep(1)

url = str()
for i in py_obj['data']['dash']['video']:
    if '1080' in quality_list[quality] and i['height'] == 1080:
        url = i['baseUrl']
        break
    elif '720' in quality_list[quality] and i['height'] == 720:
        url = i['baseUrl']
        break
    elif '480' in quality_list[quality] and i['height'] == 480:
        url = i['baseUrl']
        break
    elif '360' in quality_list[quality] and i['height'] == 360:
        url = i['baseUrl']
        break

download('video.ms4', url)
print('视频下载完成')
sleep(3)
print('音频下载开始')
sleep(1)
url = py_obj['data']['dash']['audio'][0]['baseUrl']
download('audio.ms4', url)

print('音频下载完成')
print('开始合并音视频')
try:
    f = FFmpeg(
        inputs={'video.ms4': None, 'audio.ms4': None},
        outputs={'result.mp4': '-c:v copy -c:a ac3'}
    )
    f.run()
except:
    print('错误:请检查您电脑内是否正确安装了ffmpeg')
else:
    print('音视频合并完成，已输出至result.mp4')
system('pause')
