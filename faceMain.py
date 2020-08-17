from baiduAPI.faceSDK import faceSDK

"""
人脸识别测试逻辑：
1.创建人脸库——用户组——用户
2.添加人脸数据，对应关系为用户——多个人脸
3.人脸识别和搜索
"""

# 调用百度face
class faceTest:

    def __init__(self):
        self.facePath = 'C:\\Users\\Thinkpad\\Pictures\\个人.jpg'

    def creatUser(self, groupID):
        # 新建
        print("新建用户组")
        faceSDK(self.facePath).creatGroup(groupID)

    def creatFace(self, groupID, userID, faceNames):
        # 添加
        for faceName in faceNames:
            facePath = 'C:\\Users\\Thinkpad\\Pictures\\%s' % faceName
            print("新建人脸信息")
            print(faceSDK(facePath).faceRegist(groupID, userID))

    def searchUser(self, groupID, userID, facePath):
        # 查找
        print("人脸库中所有用户组")
        groupList = faceSDK(facePath).getGroupList()
        print(groupList["result"])
        print("人脸库%s号用户组中所有用户" % groupID)
        userList = faceSDK(facePath).getGroup(groupID)
        print(userList["result"])
        print("人脸库%s号用户组中%s号用户所有人脸信息" % (groupID, userID))
        faceList = faceSDK(facePath).getFacelist(groupID, userID)
        print(faceList["result"])

    def searchFace(self, imgPath):
        # 匹配
        print("匹配结果")
        searchResult = faceSDK(imgPath).faceSearch()
        print(searchResult["result"])

faceNames = ['001.jpg','002.jpg','003.jpg','004.jpg','个人.jpg']


imgPath = 'C:\\Users\\Thinkpad\\Pictures\\006.jpg'
# 查找
faceTest().searchUser('1', '1', imgPath)
# 添加
faceTest().creatFace('1', '1', faceNames)
# 匹配
faceTest().searchFace(imgPath)

