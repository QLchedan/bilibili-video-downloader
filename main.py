from Ui_main import *
from Ui_video_download import *
from requests import get as requests_get
from bs4 import BeautifulSoup
from ffmpy3 import FFmpeg
from demjson import decode as demjson_decode
from time import time
from json import loads as json_loads
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide2.QtCore import Signal
from _thread import start_new_thread
import sys

class VideoDownload(QDialog):
    Sig = Signal(str)
    bvid = None
    def __init__(self, parent=None):
        super(VideoDownload, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.download.clicked.connect(self.download)
        self.setWindowTitle('选择分辨率')
        
    def download(self):
        self.Sig.emit(self.ui.quality.currentText())
        self.close()

    def additem(self):
        soup = BeautifulSoup(requests_get('https://www.bilibili.com/video/' + self.bvid, verify=False).content, 'html.parser')
        scripts_list = soup.find_all('script')
        info = scripts_list[3].contents[0][20:-1] + '}'
        py_obj = demjson_decode(info)
        for i in py_obj['data']['accept_description']:
            if i != '高清 1080P+' and i != '超清 4K' and i != '高清 1080P60':
                self.ui.quality.addItem(i)
        

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.LookUp.clicked.connect(self.look_up)
        self.ui.BarrageDownload.clicked.connect(self.danmaku_download)
        self.ui.CoverDownload.clicked.connect(self.cover_download)
        self.ui.VideoDownload.clicked.connect(self.open_video_download)
        self.ui.pushButton.clicked.connect(self.set_path)
        self.cid = None
        self.bvid = None
        self.setWindowTitle('B站视频综合查询下载')
        

    def look_up(self):
        res = requests_get('https://api.bilibili.com/x/web-interface/view?bvid=' + self.ui.lineEdit.text())
        res = json_loads(res.content)
        if res['code'] == 0:
            self.ui.AV.setText('av' + str(res['data']['stat']['aid']))
            self.ui.Play.setText(str(res['data']['stat']['view']))
            self.ui.Likes.setText(str(res['data']['stat']['like']))
            self.ui.Title.setText(res['data']['title'])
            self.ui.Coins.setText(str(res['data']['stat']['like']))
            self.ui.Collection.setText(str(res['data']['stat']['favorite']))
            self.ui.Uploder.setText(res['data']['owner']['name'])
            self.cid = res['data']['cid']
            self.bvid = self.ui.lineEdit.text()
            
    def set_path(self):
        a = QFileDialog.getExistingDirectory(QMainWindow(), "选择文件夹")
        self.ui.lineEdit_2.setText(a)
        
    def open_video_download(self):
        vd = VideoDownload()
        vd.Sig.connect(self.video_download)
        print(self.bvid)
        vd.bvid = self.bvid
        vd.additem()
        vd.exec_()

    def video_download(self, connect):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
            'Referer': 'http://www.bilibili.com/',
        }
        def merge(name):
            self.ui.listWidget.addItem('音视频合并开始')
            f = FFmpeg(
                inputs={name[0]: None, name[1]: None},
                outputs={name[0].replace('video.ms4', 'result.mp4'): '-c:v copy -c:a ac3'}
            )
            f.run()
            self.ui.listWidget.addItem('音视频合并结束')
            self.ui.listWidget.addItem('请在' + name[0].replace('video.ms4', 'result.mp4') + '查看输出结果')
        def download(name, url):
            for k in range(len(url)):
                r = requests_get(url[k], stream=True, headers=headers, verify=False)
                print(r)
                length = float(r.headers['content-length'])
                f = open(name[k], 'wb')
                count = 0
                time1 = time()
                for chunk in r.iter_content(chunk_size = 1024):
                    if chunk:
                        f.write(chunk)
                        count += len(chunk)
                        if time() - time1 > 0.25:
                            p = count / length * 100
                            self.ui.listWidget.addItem(name[k] + ': ' + str(round(p, 2)) + '%')
                            time1 = time()
                self.ui.listWidget.addItem(name[k] + '下载完成')
                f.close()
            merge(name)
        soup = BeautifulSoup(requests_get('https://www.bilibili.com/video/' + self.bvid, verify=False).content, 'html.parser')
        scripts_list = soup.find_all('script')
        info = scripts_list[3].contents[0][20:-1] + '}'
        py_obj = demjson_decode(info)
        url = str()
        print(connect)
        for i in py_obj['data']['dash']['video']:
            if '1080' in connect and i['height'] == 1080:
                url = i['baseUrl']
                break
            elif '720' in connect and i['height'] == 720:
                url = i['baseUrl']
                break
            elif '480' in connect and i['height'] == 480:
                url = i['baseUrl']
                break
            elif '360' in connect and i['height'] == 360:
                url = i['baseUrl']
                break
        l = [url]
        l.append(py_obj['data']['dash']['audio'][0]['baseUrl'])
        path = [self.ui.lineEdit_2.text() + '\\video.ms4', self.ui.lineEdit_2.text() + '\\audio.ms4']
        start_new_thread(download, (path, l))

    def cover_download(self):
        def download(url, name):
            r = requests_get(url).content
            with open(name, 'wb') as f:
                f.write(r)
            self.ui.listWidget.addItem('请在' + name + '查看输出结果')
        res = requests_get('https://api.bilibili.com/x/web-interface/view?bvid=' + self.ui.lineEdit.text())
        res = json_loads(res.content)
        #print(res)
        if res['code'] == 0:
            start_new_thread(download, (res['data']['pic'], self.ui.lineEdit_2.text() + '\\cover.jpg'))

    def danmaku_download(self):
        if self.cid != None:
            r = requests_get('https://api.bilibili.com/x/v1/dm/list.so?oid=' + str(self.cid))
            with open(self.ui.lineEdit_2.text() + '\\danmoku.xml', 'wb') as f:
                f.write(r.content)
        self.ui.listWidget.addItem('请在' + self.ui.lineEdit_2.text() + '\\danmoku.xml' + '查看输出结果')


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())