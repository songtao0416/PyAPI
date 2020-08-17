from aip import AipOcr

""" 你的 APPID AK SK """
APP_ID = '16447162'
API_KEY = 'lcwtofSmIxXspdkCblY1xTKf'
SECRET_KEY = "WGvqs6SOeu3s8V9W804zndcTuuuIer6j"

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

""" 读取图片 """


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


image = get_file_content('C:\\Users\\Thinkpad\\Pictures\\test.png')
""" 调用通用文字识别, 图片参数为本地图片 """
client.basicGeneral(image)


""" 如果有可选参数 """
options = {}
options["language_type"] = "CHN_ENG"
options["detect_direction"] = "true"
options["detect_language"] = "true"
options["probability"] = "true"

""" 带参数调用通用文字识别, 图片参数为本地图片 """
""" 调用api"""
picture_result = client.basicGeneral(image, options)  # 返回识别结果

""" 调用通用文字识别, 图片参数为远程url图片 """
url = "https//www.x.com/sample.jpg"
client.basicGeneralUrl(url)
""" 如果有可选参数 """
options = {}
options["language_type"] = "CHN_ENG"
options["detect_direction"] = "true"
options["detect_language"] = "true"
options["probability"] = "true"

""" 带参数调用通用文字识别, 图片参数为远程url图片 """
client.basicGeneralUrl(url, options)
print(picture_result)  # 打印