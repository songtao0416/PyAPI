import re
import requests
import json

class connectAPI:

    def __init__(self):
        self.urlPost = "http://ip:port/shujugongchang/api/ie/abstract"
        headers = {"Host": "vip-api.shudigongchang.com", "Content-type": "text/json"}
        str = "同一个取值文本中，可能既有规范单元，也有数值单元，还有纯文本单元，对应多个不同类型的参数。建议：（2）不同参数的取值文本相同不同参数对应的取值行相同，导致不同参数重复取值，或同一参数取值范围过大。（3）文档中不能与模板参数对应的内容建议：提取并创建为新参数；"
        self.dataPost = {"text": str}
        self.data = requests.post(url=self.urlPost, data=self.dataPost, headers=headers)
        print(self.data.text)

connectAPI()


