import os
import time
import subprocess
import xmltodict
import json
from ocr import OCRbase
import argparse


class AdbBase:
    def __init__(self, dev, p=None, w=None, f=None, log=None):
        self.dev = dev
        self.p = p
        self.w = w
        self.f = f
        self.detaillog = log

    # 根据坐标点击228 174  1000 28
    def AdbShellInputTap(self, state, x, y):
        self.printLog(state, "点击位置:" + str(x) + "|" + str(y))
        self.log("点击位置:" + str(x) + "|" + str(y))
        os.popen("adb -s %s shell input tap %s %s" % (self.dev, x, y))

        # 输入字符

    def AdbShellInputText(self, text):
        self.printLog("账号登录", "输入字符：" + str(text))
        os.popen("adb -s %s shell input text %s" % (self.dev, text))

    # 等待时间
    def TimeSleepDuration(self, x):
        time.sleep(x)

    # 保存截图到指定路径
    def AdbShellScreencapPullRm(self, path):
        # if self.p is None:
        self.printLog("截取截图", "截取图片%s" % path)
        os.popen("adb -s %s exec-out screencap -p > %s" % (self.dev, path))
        time.sleep(5)
        self.printLog("截取截图", "截取图片%s完成" % path)
        # 保存截图到指定路径

    # //查看手机上第三方应用的packageName
    # //adb shell pm list packages -3
    def AdbShellPmListPackages(self):
        data = subprocess.Popen("adb -s %s shell pm list packages -3" % self.dev, shell=True, stdout=subprocess.PIPE,
                                encoding='utf-8')
        return data.stdout.read()

    def __adbDump(self, apkName):
        self.printLog("dump文件", "加载xml文件")
        path = os.getcwd()
        if self.w is not None:
            path = self.w
        # os.path.abspath()
        subprocess.Popen(
            "adb -s %s shell uiautomator dump --compressed /sdcard/%s.xml > sdcard/info.txt" % (self.dev, apkName))
        time.sleep(2)
        os.popen("adb -s %s pull /sdcard/%s.xml %s >log.txt" % (self.dev, apkName, path))
        time.sleep(2)
        self.printLog("dump文件", "加载xml文件完成")
        if "xml" in path:
            return path
        else:
            return os.path.join(path, "%s.xml" % apkName)

    # 根据字符，在dump文件中查找对应坐标 path:文件地址，不包括文件名，返回是：[[224.0, 174.5], [968.0, 468.5]]
    def adbDumpTap(self, text, path):
        self.printLog("账号登录", "点击%s" % text)
        self.log("根据文字点击" + "“" + str(text) + "”")
        apkname, _ = self.getAPKInfo(path)
        file = self.__adbDump(apkname)
        json_data = self.xml_to_json(file)
        self.__cyclefromNode(json_data["hierarchy"], text)

    def __cyclefromNode(self, json, text):
        # 遍历每个Node节点
        if isinstance(json, dict) and 'node' in json.keys():
            self.__cyclefromNode(json['node'], text)

        elif isinstance(json, list) or isinstance(json, tuple):
            for item in json:
                self.__cyclefromNode(item, text)
        else:
            # print(json)
            if text == json["@text"]:
                point = json["@bounds"].split('][')[0][1:].split(",")
                # print(point)
                self.AdbShellInputTap("账号登录", point[0], point[1])
                return True

    # xml文件转换成json
    def xml_to_json(self, xml):
        xml_file = open(xml, "r", encoding="utf-8")
        xml_str = xml_file.read()
        xml_parse = xmltodict.parse(xml_str)
        json_str = json.dumps(xml_parse, ensure_ascii=False, indent=1)
        json_data = json.loads(json_str)
        return json_data

    # 返回packageName 和 launcher_act
    def getAPKInfo(self, filePath):
        self.log("获取apk信息")
        data = subprocess.Popen("aapt dump badging %s | findstr package" % filePath,
                                shell=True, stdout=subprocess.PIPE, encoding='utf-8')
        apkname = data.stdout.read().split('\'')[1]

        data3 = subprocess.Popen("aapt dump badging %s | findstr launchable" % filePath,
                                 shell=True, stdout=subprocess.PIPE, encoding='utf-8')
        launchable_activity = data3.stdout.read().split('\'')[1]

        return apkname, launchable_activity

    # 安装apk
    def install_apk(self, path):
        result = subprocess.Popen("adb -s %s install %s" % (self.dev, path),
                                  shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.read()
        if 'Success' in result:
            return True
        else:
            return False

    # 卸载apk
    def uninstall_apk(self, path):
        apkname, _ = self.getAPKInfo(path)
        subprocess.Popen("adb -s %s uninstall %s" % (self.dev, apkname))

    # 启动apk
    def start_apk(self, path):
        self.printLog("启动apk", "启动apk %s" % path)
        self.log("启动apk")
        try:
            apkname, activity = self.getAPKInfo(path)
            subprocess.Popen(
                "adb -s {0} shell am start -S -n {1}/{2} > sdcard/info.txt".format(self.dev, apkname, activity))
            self.log("启动成功")
            self.printLog("启动apk", "启动apk成功")
        except:
            err = "apk路径错误"
            return err

    # 判断是否存在包名
    def findIsExitPackage(self, path):
        apkname, _ = self.getAPKInfo(path)
        data = self.AdbShellPmListPackages()
        for i in data:
            if apkname in i:
                return True
            else:
                return False

    # 判断模拟器是否在运行中
    def detectIsWorking(self):
        result = subprocess.Popen("adb shell dumpsys activity | grep mResumedActivity",
                                  shell=True, stdout=subprocess.PIPE, encoding='utf-8')
        result = result.stdout.read()
        if result != None and 'com.vphone.launcher/.Launcher' in result:
            return False
        else:
            return True

    # 关闭当前应用
    def killCurrentGame(self, path):
        apkname, _ = self.getAPKInfo(path)
        subprocess.Popen("adb -s %s shell am force-stop %s" % (self.dev, apkname))
        self.log("关闭应用")
        self.printLog("关闭应用", "关闭应用%s" % path)

    # 打印log到指定地址
    def log(self, info):
        if not self.f:
            return
        current_time = time.strftime("%Y-%m-%d/%H:%M:%S", time.localtime(time.time()))
        # print("%s" % i)
        tag = "adb[" + str(current_time) + "]:  "
        with open(self.f, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
            f.write(str(tag) + str(info) + "\n")

    def printLog(self, state, info):
        if not self.detaillog:
            return
        else:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            value = {"time": current_time, "level": "info", "stage": state, "msg": info}
            print(json.dumps(value))


def allStart():
    parser = argparse.ArgumentParser(description="powered from apson")
    parser.add_argument('-s', '--sid', help='输入设备id')
    parser.add_argument('-p', '--picturepath', help='图片地址')
    parser.add_argument('-apkPath', '---apkPath', help='apk路径')
    parser.add_argument('-w', '---windowpath', help='window.xml 路径')
    parser.add_argument('-d', '---debugfilepath', help='log文件路径')
    parser.add_argument('-l', '---detaillog', help='是否需要输出日志')
    args = parser.parse_args()

    sid = args.sid
    picture = args.picturepath
    apkPath = args.apkPath
    windowpath = args.windowpath
    debugfilepath = args.debugfilepath
    log = args.detaillog

    adb = AdbBase(sid, picture, windowpath, debugfilepath, log)
    ocr = OCRbase(picture)
    adb.log(10 * "-" + '初始化信息' + 10 * "-")

    adb.log("sid:" + sid)
    adb.log("picturepath:" + picture)
    adb.log("apkPath:" + apkPath)
    adb.log("windowpath:" + windowpath)
    return picture, apkPath, adb, ocr


def dataRe(state=0, err="", datas=""):
    if state == 1 or state is None:
        value = {
            "state": state,
            "data": {
                "districtName": "",
            },
            "err": err
        }
    else:
        value = {
            "state": state,
            "data": {
                "districtName": datas,
            },
            "err": ""
        }
    return value

# 测试点击
# AdbBase("127.0.0.1:62001").adbDumpTap("帐号登录", r"D:\bao\apk\20201130\222.apk")
# time.sleep(1)
# Adb_base("127.0.0.1:7555").AdbShellInputTap(1000, 28)
# time.sleep(1)
# Adb_base("127.0.0.1:7555").AdbShellInputText("ssss")
# AdbBase("127.0.0.1:62001").AdbShellScreencapPullRm(r"D:\bao\1\0531落地页")
# print(Adb_base("127.0.0.1:7555").AdbShellPmListPackages())
# print(AdbBase("127.0.0.1:7555").Adbdump(r"D:\bao\1\0531落地页"))
# print(AdbBase("127.0.0.1:7555").xml_to_json(r"D:\bao\1\0531落地页\window_dump.xml"))
# print(AdbBase("127.0.0.1:7555").Adbdump_Tap(r"D:\bao\1\0531落地页", "微信"))
# a = AdbBase("127.0.0.1:62001")
# a.adbDumpTap("游客登录")
# a= AdbBase("127.0.0.1:62001").install_apk(r"D:\bao\apk\20201130\222.apk")

# print(a)

# AdbBase("127.0.0.1:62027").install_apk(r"D:\bao\apk\20201130\222.apk")
