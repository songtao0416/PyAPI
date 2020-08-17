from baiduAPI.ocrSDK import ocrSDK
from baiduAPI.faceSDK import faceSDK

# 调用百度OCR
def getocrSDK():
    ocrResult = ocrSDK(iamgePath).generalOCRHigh()
    for x in ocrResult['words_result']:
        print(x)
    return ocrResult

# 调用百度face
def getfaceSDK():
    # 检测
    print("人脸监测结果")
    print(faceSDK(facePath).faceDetection())
    # 新建
    print("新建用户组")
    faceSDK(facePath).creatGroup('2')
    print("新建人脸信息")
    print(faceSDK(facePath).faceRegist('1', '1'))
    # 查找
    print("人脸库中所有用户组")
    groupList = faceSDK(facePath).getGroupList()
    print(groupList["result"])
    print("人脸库1号用户组中所有用户")
    userList = faceSDK(facePath).getGroup('1')
    print(userList["result"])
    print("人脸库1号用户组中1号用户所有人脸信息")
    faceList = faceSDK(facePath).getFacelist('1', '1')
    print(faceList["result"])
    # 匹配
    print("匹配结果")
    searchResult = faceSDK(facePath).faceSearch()
    print(searchResult["result"])

if __name__ == '__main__':
    iamgePath = 'C:\\Users\\Thinkpad\\Pictures\\test.png'
    facePath = 'C:\\Users\\Thinkpad\\Pictures\\个人.jpg'
    # getocrSDK()
    getfaceSDK()
