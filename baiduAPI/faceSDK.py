
from config.baiduConfig import apiConfig
from aip import AipFace
import base64


class faceSDK:
    """
    通过SDK调用百度的人脸识别api，具体如下：

    用户族组操作： 'getGroup', 'getGroupList', groupDelete','creatGroup'
    用户操作： 'getuser', ' 'userDelete'，
    人脸操作： 'faceUpdate', 'getFacelist','faceDelete'：更新/查询列表/删除
         faceUpdate, 人脸更新,用于对人脸库中指定用户，更新其下的人脸图像。
         faceDelete, 人脸删除，用于从人脸库中删除一个用户。

    faceDetection，人脸检测：检测图片中的人脸并标记出位置信息;
    faceSearch, 1：N人脸搜索：也称为1：N识别，在指定人脸集合中，找到最相似的人脸；
                1：N人脸认证：基于uid维度的1：N识别，由于uid已经锁定固定数量的人脸，所以检索范围更聚焦；
    faceRegist, 用于从人脸库中新增用户，可以设定多个用户所在组，及组内用户的人脸图;人脸库、用户组、用户、用户下的人脸层级关系
    'aliveCheck', 在线活体检测
    ‘IDCheck’，身份验证， 质量检测（可选）活体检测（可选）公安验证（必选）
    'userCopy', 复制用户，用于将已经存在于人脸库中的用户复制到一个新的组。
    'faceMatch', 人脸对比， 两张人脸图片相似度对比：比对两张图片中人脸的相似度，并返回相似度分值
    'faceSearchMulti'，人脸搜索 M:N 识别， 待识别的图片中，存在多张人脸的情况下，支持在一个人脸库中，一次请求，同时返回图片中所有人脸的识别结果。
    """

    def __init__(self, filePath):
        self.filePath = filePath
        self.apiConfig = apiConfig().faceAPI
        self.client = self.aipFace()
        self.image = self.getImage()
        self.imageType = "BASE64"

    def aipFace(self):
        APPID = self.apiConfig["APPID"]
        APIKey = self.apiConfig["APIKey"]
        SecretKey = self.apiConfig["SecretKey"]
        client = AipFace(APPID, APIKey, SecretKey)
        return client

    def getImage(self):
        image = str(base64.b64encode(open(self.filePath,'rb').read()), 'utf-8')
        return image

    # 返回人脸检测数据
    def faceDetection(self):
        """ 如果有可选参数 """
        options = {}
        options[
            "face_field"] = "age"  # 包括age,beauty,expression,face_shape,gender,glasses,landmark,landmark72，landmark150，race,quality,eye_status,emotion,face_type信息 逗号分隔. 默认只返回face_token、人脸框、概率和旋转角度
        options["max_face_num"] = 1  # 最多处理人脸的数目，默认值为1，仅检测图片中面积最大的那个人脸；最大值10，检测图片中面积最大的几张人脸
        options[
            "face_type"] = "LIVE"  # LIVE表示生活照：通常为手机、相机拍摄的人像图片、或从网络获取的人像图片等IDCARD表示身份证芯片照：二代身份证内置芯片中的人像照片 WATERMARK表示带水印证件照
        options[
            "liveness_control"] = "LOW"  # 活体检测控制 NONE: 不进行控制 LOW:较低的活体要求(高通过率 低攻击拒绝率) NORMAL: 一般的活体要求(平衡的攻击拒绝率, 通过率) HIGH: 较高的活体要求(高攻击拒绝率 低通过率) 默认NONE
        return self.client.detect(self.image, self.imageType)

    def faceSearch(self):
        """ 如果有可选参数 """
        options = {}
        options["max_face_num"] = 3  # 最多处理人脸的数目,默认值为1(仅检测图片中面积最大的那个人脸) 最大值10
        options["match_threshold"] = 80  # 匹配阈值（设置阈值后，score低于此阈值的用户信息将不会返回） 最大100 最小0 默认80 此阈值设置得越高，检索速度将会越快，推荐使用默认阈值80
        options["quality_control"] = "NORMAL"
        options["liveness_control"] = "LOW"
        options["user_id"] = "233451"  # 当需要对特定用户进行比对时，指定user_id进行比对。即人脸认证功能。
        options["max_user_num"] = 3
        # 从指定的group中进行查找 用逗号分隔，上限20个
        groupIdList = "1,2"
        return self.client.search(self.image, self.imageType, groupIdList)

    def faceSearchMulti(self):
        """ 如果有可选参数 """
        options = {}
        options["max_face_num"] = 3
        options["match_threshold"] = 70
        options["quality_control"] = "NORMAL"
        options["liveness_control"] = "LOW"
        options["max_user_num"] = 3
        groupIdList = "1,2"
        return self.client.multiSearch(self.image, self.imageType, groupIdList)

    def creatGroup(self, groupId):
        self.client.groupAdd(groupId)

    def faceRegist(self, groupId, userId):
        # 结构：至多100人脸库——多个用户组——多个用户
        # 每个开发者账号可以创建100个appid,对应人脸库；
        # 每个appid对应一个人脸库，且不同appid之间，人脸库互不相通；
        # 一个uid可以有多个face_toke
        """ 如果有可选参数 """
        options = {}
        options["user_info"] = "user's info"
        options["quality_control"] = "NORMAL"
        options["liveness_control"] = "LOW"
        options["action_type"] = "REPLACE"
        # todo
        # 人脸质量判断
        # faceData = self.faceDetection()
        # if faceData['++biur'] <= 0.7:
        print("人脸信息添加成功")
        return self.client.addUser(self.image, self.imageType, groupId, userId)

    def faceUpdate(self, groupId, userId):
        self.client.updateUser(self.image, self.imageType, groupId, userId)

    def faceDelete(self, userId, groupId):
        # 	需要删除的人脸图片token，（由数字、字母、下划线组成）长度限制64B
        faceToken = "face_token_23123"
        self.client.faceDelete(userId, groupId, faceToken)

    def userDelete(self, groupId, userId):
        self.client.deleteUser(groupId, userId)

    def groupDelete(self, groupId):
        self.client.groupDelete(groupId)

    def getuser(self, userId, groupId):
        return self.client.getUser(userId, groupId)

    def getFacelist(self, userId, groupId):
        return self.client.faceGetlist(userId, groupId)

    def getGroup(self, groupId):
        """ 如果有可选参数 """
        options = {}
        options["start"] = 0
        options["length"] = 50
        return self.client.getGroupUsers(groupId)

    def getGroupList(self):
        return self.client.getGroupList()

    def userCopy(self, userID):
        """ 如果有可选参数 """
        options = {}
        options["src_group_id"] = "11111"   #从指定组里复制信息
        options["dst_group_id"] = "222222"  #需要添加用户的组id
        return self.client.userCopy(userID)

    def IDCheck(self,idCardNumber,name):
        score = self.client.personVerify(self.image, self.imageType, idCardNumber, name)
        if score["score"] >= 0.8:
            print("通过验证")
            return "yes"
        else:
            return "no"

    def aliveCheck(self):
        return self.client.faceverify([self.image, self.imageType])

    def faceMatch(self):
        return self.client.match([self.image, self.imageType])



