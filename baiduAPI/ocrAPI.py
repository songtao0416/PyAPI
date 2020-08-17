import json
import requests
import base64
import urllib.parse
from config.baiduConfig import apiConfig

class baiduAPI:

    def __init__(self):
        self.apiConfig = apiConfig().ocrAPI
        self.imgFile = 'C:\\Users\\Thinkpad\\Pictures\\test.png'
        self.token = self.getToken()
        self.image = self.getImage()
        self.getAPI()

    def getToken(self):
        """
        grant_type： 必须参数，固定为client_credentials；
        client_id： 必须参数，应用的API Key；
        client_secret： 必须参数，应用的Secret Key；
        """
        base_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
        APPID=self.apiConfig["APPID"]
        APIKey=self.apiConfig["APIKey"]
        SecretKey=self.apiConfig["SecretKey"]
        url = base_url % (APIKey, SecretKey)
        data = requests.post(url)
        token = data.json()['access_token']
        print(data.json()['access_token'])
        print(data.json()["expires_in"])
        return token

    def getImage(self):
        # 读取图片并进行base64加密
        body = base64.b64encode(open(self.imgFile, 'rb').read())
        # 进行urlencode
        data = urllib.parse.urlencode({'image': body})
        return data


    def getAPI(self):
        url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=%s" % self.token
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        # bodyDict = dict(image=self.image)
        data = requests.post(url, data=self.image, headers=headers)
        print(data.json())

baiduAPI()