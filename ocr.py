from aip import AipOcr
import requests
import time
import hashlib
import base64
import json
import os
import cv2
from PIL import Image
import numpy as np

# baidu_ocr
_APP_ID_baidu = '17975398'
_API_KEY_baidu = 'n8bGMLwndukfywu18yKLuNYI'
_SECRET_KEY_baidu = 'fNqBSM0A9gRloci2kv139ZlxL7aGSfor'
_client = AipOcr(_APP_ID_baidu, _API_KEY_baidu, _SECRET_KEY_baidu)

# 讯飞ocr
URL = "http://webapi.xfyun.cn/v1/service/v1/ocr/general"
APPID = "5fd066f5"
API_KEY = "b9db4d674b5f3af780f2ab665ec67527"


class OCRbase:
    # 默认不裁剪，如果有裁剪需求，isFix 为True 时是裁剪模式，需要传入坐标
    def __init__(self, filepath, isFix=False, topX=0, bottomX=0, topY=0, bottomY=0):
        self.filepath = filepath
        # print("初始化文件地址：", self.filepath)
        if isFix:
            self.filepath = self.__opencv_Picture(topX, bottomX, topY, bottomY)
            # print("裁剪后文件地址：", self.filepath)

    def _get_file_content(self):
        # print("打开文件地址：", self.filepath)
        with open(self.filepath, 'rb') as fp:
            return fp.read()

    # basicAccurate 高精准 basicGeneral 通用
    # 高精准识别图片用于识别区服，不带坐标
    def ocr_QFdata(self):
        try:
            image = self._get_file_content()
            resluts = _client.basicAccurate(image)
            # print("未处理前数据：", resluts)
            return resluts["words_result"][0]["words"]
        except:
            state = "小图识别错误，请查看大图"
            return state

    # 返回坐标 普通版
    def ocr_Tap(self, value):
        tap = []
        image = self._get_file_content()
        result = _client.general(image)
        data = result["words_result"]
        return [[i["location"]['left'], i["location"]['top']] for i in data if value in i['words']]

    # 返回坐标 精准版
    def ocr_Tap2(self, value):
        tap = []
        image = self._get_file_content()
        result = _client.accurate(image)
        data = result["words_result"]
        return [[i["location"]['left'], i["location"]['top']] for i in data if value in i['words']]

    def _getHeader(self):
        curTime = str(int(time.time()))
        #  支持语言类型和是否开启位置定位(默认否)
        param = {"language": "cn|en", "location": "true"}
        param = json.dumps(param)
        paramBase64 = base64.b64encode(param.encode('utf-8'))

        m2 = hashlib.md5()
        str1 = API_KEY + curTime + str(paramBase64, 'utf-8')
        m2.update(str1.encode('utf-8'))
        checkSum = m2.hexdigest()
        # 组装http请求头
        header = {
            'X-CurTime': curTime,
            'X-Param': paramBase64,
            'X-Appid': APPID,
            'X-CheckSum': checkSum,
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        }
        return header

    # 讯飞返回总数据
    def get_data_xunfei(self):
        image = self._get_file_content()
        f1_base64 = str(base64.b64encode(image), 'utf-8')
        data = {
            'image': f1_base64
        }
        r = requests.post(URL, data=data, headers=self._getHeader())
        result = str(r.content, 'utf-8')
        return result

    # 讯飞返回字符坐标 {'x': 596, 'y': 570}
    def ocr_Tapdata_xf(self, value):
        data = self.get_data_xunfei()
        data = json.loads(data)
        b = data["data"]["block"]
        for i in b:
            for z in i["line"]:
                for k in z["word"]:
                    if value in k["content"]:
                        return k["location"]["top_left"]

    # 讯飞返回区服
    def ocr_QFdata_xf(self):
        data = self.get_data_xunfei()
        data = json.loads(data)
        b = data["data"]["block"]
        for i in b:
            for z in i["line"]:
                for k in z["word"]:
                    return k["content"]

    # opencv进行屏幕截取并重新生成新图片如：hmy.png->hmy2.png
    def __opencv_Picture(self, x1, x2, y1, y2):
        path = self.filepath
        img_g = cv2.imread(path)
        # print("开始剪切:", path)
        if img_g is None:  # 图片路径存在正常图片，但是cv2 读取图片报错
            img = Image.open(path)
            img = np.asanyarray(img)
            img_g = img[:, :, [2, 1, 0]]  # 原本是RGB->BGR
        img = img_g[y1:y2, x1:x2]
        # print("剪切完成")
        new_file = path.split(".")[0]
        # print("new_file:", new_file)
        new_picture = new_file + "_refix" + ".png"
        cv2.imwrite(new_picture, img)
        # print("new_picture:", new_picture)
        return new_picture

# 测试
# print(OCRbaidu(r"D:\PyCharm\space\testApi\picture\hmy2.png").ocr_QFdata())
# print(OCRbaidu(r"D:\PyCharm\space\testApi\picture\hmy.png").ocr_Tap2("进入游戏"))
# print(OCRbase(r"D:\PyCharm\space\testApi\picture\hmy.png").ocr_QFdata_xf("进入游戏"))
# print(OCRbase(r"/Users/apson/Desktop/30600.png").ocr_Tap('进入游戏')))
# data = OCRbase(r"D:\test", isFix=True, topX=558, bottomX=983, topY=515, bottomY=567).ocr_QFdata()
# print(data)
