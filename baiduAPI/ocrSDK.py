from config.baiduConfig import apiConfig
from aip import AipOcr

# 通过百度SDK调用文字识别接口，只能识别本地图片，需提供图片地址
# 传入图片地址，传出OCR结果
class ocrSDK:
    """
    通过百度SDK调用文字识别接口，OCR功能包括：
    'generalOCR', 通用文字识别；
    'generalOCRHigh',通用文字识别（高精度）；
    'generalOCRPos', 通用文字识别（含位置信息版）；
    'generalOCRPosHigh', 通用文字识别（含位置高精度版）；
    'generalOCRUncom', 通用文字识别（含生僻字版）；
    'networkOCR',网络图片文字识别：识别一些网络上背景复杂，特殊字体的文字
    'networkOCRPos',网络图片文字识别（含位置版）：
    'IDcardOCR',身份证识别；身份证识别包括正面和背面
    'bankcardOCR',银行卡识别：识别银行卡并返回卡号和发卡行
    'diverLicenseOCR',驾驶证识别：对机动车驾驶证所有关键字段进行识别
    'drivingLicenseOCR', 行驶证识别：对机动车行驶证正本所有关键字段进行识别
    'carLicenseOCR',车牌识别：识别机动车车牌，并返回签发地和号牌
    'businessLicenseOCR', 营业执照识别：识别营业执照，并返回关键字段的值，包括单位名称、法人、地址、有效期、证件编号、社会信用代码等
    'billOCR',通用票据识别：识别医疗票据、发票、的士票、保险保单等票据类图片中的所有文字
    'customOCR', 自定义模板文字识别：使用该产品快速制作模板，进行识别
    'tableSyncOCR'表格文字识别同步接口：自动识别表格线及表格内容，结构化输出表头、表尾及每个单元格的文字内容
    'tableRequestOCR',表格文字识别:调用表格识别请求，获取请求id之后轮询调用表格识别获取结果的接口
    'docLayOCR', 文档版面分析与识别：可对文档版面进行分析，输出图、表、标题、文本的位置，并输出分版块内容的OCR识别结果
    'panelOCR',仪器仪表盘读数识别：适用于不同品牌、不同型号的仪器仪表盘读数识别，广泛适用于各类血糖仪、血压仪、燃气表、电表等，可识别表盘上的数字、英文、符号，支持液晶屏、字轮表等表型
    """

    def __init__(self, imagePath):
        self.filePath = imagePath
        self.apiConfig = apiConfig().ocrAPI
        self.client = self.aipOCR()
        self.image = self.getImage()

    def aipOCR(self):
        APPID = self.apiConfig["APPID"]
        APIKey = self.apiConfig["APIKey"]
        SecretKey = self.apiConfig["SecretKey"]
        client = AipOcr(APPID, APIKey, SecretKey)
        return client

    # 读取图片
    def getImage(self):
        with open(self.filePath, 'rb') as fp:
            image = fp.read()
            return image

    # 调用通用文字识别, 图片参数为本地图片
    def generalOCR(self):
        """ 可选参数分别为:输出语言、图像朝向、文本语言、每一行置信度 """
        options = {}
        options["language_type"] = "CHN_ENG"
        options["detect_direction"] = "true"
        options["detect_language"] = "true"
        options["probability"] = "true"
        """
        字段	                必选	类型	    说明
        direction	        否	number	图像方向，当detect_direction=true时存在。
                                        - -1:未定义，
                                        - 0:正向，
                                        - 1: 逆时针90度，
                                        - 2:逆时针180度，
                                        - 3:逆时针270度
        log_id	            是	number	唯一的log id，用于问题定位
        words_result_num	是	number	识别结果数，表示words_result的元素个数
        words_result	    是	array	定位和识别结果数组
        +words	            否	string	识别结果字符串
        probability	        否	object	行置信度信息；如果输入参数 probability = true 则输出
        +average	        否	number	行置信度平均值
        +variance	        否	number	行置信度方差
        +min	            否	number	行置信度最小值
        """
        return self.client.basicGeneral(self.image)

    # todo
    def generalOCRHigh(self):
        """ 如果有可选参数 """
        options = {}
        options["detect_direction"] = "true"
        options["probability"] = "true"
        return self.client.basicAccurate(self.image)

    def generalOCRPos(self):
        """ 如果有可选参数 """
        options = {}
        options["recognize_granularity"] = "big"
        options["language_type"] = "CHN_ENG"
        options["detect_direction"] = "true"
        options["detect_language"] = "true"
        options["vertexes_location"] = "true"
        options["probability"] = "true"
        return self.client.general(self.image)

    def generalOCRPosHigh(self):
        """ 如果有可选参数 """
        options = {}
        options["recognize_granularity"] = "big"
        options["detect_direction"] = "true"
        options["vertexes_location"] = "true"
        options["probability"] = "true"
        return self.client.accurate(self.image)

    def generalOCRUncom(self):
        """ 如果有可选参数 """
        options = {}
        options["language_type"] = "CHN_ENG"
        options["detect_direction"] = "true"
        options["detect_language"] = "true"
        options["probability"] = "true"
        return self.client.enhancedGeneral(self.image)

    def networkOCR(self):
        """ 如果有可选参数 """
        options = {}
        options["detect_direction"] = "true"
        options["detect_language"] = "true"
        return self.client.webImage(self.image)

    def networkOCRPos(self):
        return self.client.webimageLoc(self.image)

    def IDcardOCR(self):
        """ 如果有可选参数 """
        options = {}
        options["detect_direction"] = "true"    #是否检测图像朝向
        options["detect_risk"] = "false"        # 是否开启身份证风险类型(身份证复印件、临时身份证、身份证翻拍、修改过的身份证)功能
        idCardSide = "front"   # front：身份证含照片的一面；back：身份证带国徽的一面
        return self.client.idcard(self.image, idCardSide)

    def bankcardOCR(self):
        return self.client.bankcard(self.image)

    def diverLicenseOCR(self):
        """ 如果有可选参数 """
        options = {}
        options["detect_direction"] = "true"
        return self.client.drivingLicense(self.image)

    def drivingLicenseOCR(self):
        """ 如果有可选参数 """
        options = {}
        options["detect_direction"] = "true"
        options["vehicle_license_side"] = "front"  #- front：识别行驶证主页 - back：识别行驶证副页
        return self.client.vehicleLicense(self.image, options)

    def carLicenseOCR(self):
        return self.client.licensePlate(self.image)

    def businessLicenseOCR(self):
        return self.client.businessLicense(self.image)

    def billOCR(self):
        """ 如果有可选参数 """
        options = {}
        options["recognize_granularity"] = "big"
        options["probability"] = "true"
        options["accuracy"] = "normal"
        options["detect_direction"] = "true"
        return self.client.receipt(self.image)

    def customOCR(self):
        return self.client.custom(self.image)

    def tableSyncOCR(self):
        return self.client.form(self.image)

    def tableRequestOCR(self):
        """ 如果有可选参数 """
        options = {}
        options["result_type"] = "json"     #期望获取结果的类型，取值为“excel”时返回xls文件的地址，取值为“json”时返回json格式的字符串,默认为”excel”
        requestID = self.client.tableRecognitionAsync(self.image)
        return self.client.getTableRecognitionResult(requestID)

    def docLayOCR(self):
        return self.client.docAnalysis(self.image)

    def panelOCR(self):
        return self.client.meter(self.image)


