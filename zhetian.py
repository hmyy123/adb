from ocr import OCRbase
import time
import adb
import json

picture, apkPath, devices, ocr = adb.allStart()
name, _ = devices.getAPKInfo(apkPath)


# 判断我在江湖公告
def is_notice(data):
    n = 0
    while n < 3:
        if "请查看大图" in data or "区" not in data:
            time.sleep(2)
            devices.AdbShellInputTap("关闭公告", 1361, 89)
            time.sleep(2)
            devices.AdbShellScreencapPullRm(picture)
            time.sleep(2)
            qfvalue = OCRbase(picture, isFix=True, topX=558, bottomX=983, topY=515, bottomY=567)
            time.sleep(2)
            data = qfvalue.ocr_QFdata()
            n += 1
        else:
            break
    return data


# 判断其他公告
def is_notice_other(data):
    n = 0
    while n < 3:
        if "请查看大图" in data or "国" not in data:
            time.sleep(2)
            devices.AdbShellInputTap("关闭公告", 1327, 94)
            time.sleep(2)
            devices.AdbShellScreencapPullRm(picture)
            time.sleep(2)
            qfvalue = OCRbase(picture, isFix=True, topX=1007, bottomX=1333, topY=447, bottomY=503)
            time.sleep(2)
            data = qfvalue.ocr_QFdata()
            n += 1
        else:
            break
    return data


def rule():
    # 遮天
    devices.start_apk(apkPath)
    time.sleep(100)
    devices.AdbShellInputTap("点击用户协议", 528, 589)
    time.sleep(2)
    devices.adbDumpTap("游客登录", apkPath)
    time.sleep(5)
    devices.AdbShellInputTap("关闭手机绑定", 1080, 225)
    time.sleep(2)
    devices.AdbShellInputTap("关闭公告", 1361, 89)
    time.sleep(2)
    devices.AdbShellScreencapPullRm(picture)
    time.sleep(2)
    qfvalue = OCRbase(picture, isFix=True, topX=558, bottomX=983, topY=515, bottomY=567)
    time.sleep(2)
    data = qfvalue.ocr_QFdata()
    if "正在" in data:
        time.sleep(2)
        devices.AdbShellInputTap("点击进入游戏", 777, 668)
        time.sleep(2)
        devices.AdbShellInputTap("点击用户协议", 528, 589)
        time.sleep(2)
        devices.adbDumpTap("游客登录", apkPath)
        time.sleep(5)
        devices.AdbShellInputTap("关闭手机绑定", 1080, 225)
        time.sleep(2)
        devices.AdbShellInputTap("关闭公告", 1361, 89)
        time.sleep(2)
        devices.AdbShellScreencapPullRm(picture)
        time.sleep(2)
        qfvalue = OCRbase(picture, isFix=True, topX=558, bottomX=983, topY=515, bottomY=567)
        time.sleep(2)
        data = qfvalue.ocr_QFdata()
    return is_notice(data)

    # 疯狂走位
    # devices.start_apk(apkPath)
    # time.sleep(100)
    # devices.adbDumpTap("快速游戏", apkPath)
    # time.sleep(5)
    # devices.AdbShellInputTap("关闭公告", 1361, 89)
    # time.sleep(2)
    # devices.AdbShellScreencapPullRm(picture)
    # time.sleep(2)
    # qfvalue = OCRbase(picture, isFix=True, topX=558, bottomX=983, topY=515, bottomY=567)
    # time.sleep(3)
    # data = qfvalue.ocr_QFdata()
    # return is_notice(data)

    # 反向操作
    # devices.start_apk(apkPath)
    # time.sleep(100)
    # devices.adbDumpTap("用户注册", apkPath)
    # time.sleep(5)
    # devices.AdbShellInputTap("关闭公告", 1327, 94)
    # time.sleep(2)
    # devices.AdbShellScreencapPullRm(picture)
    # time.sleep(2)
    # qfvalue = OCRbase(picture, isFix=True, topX=1007, bottomX=1333, topY=447, bottomY=503)
    # time.sleep(3)
    # data = qfvalue.ocr_QFdata()
    # return is_notice_other(data)

    # 憨憨大作战
    # devices.start_apk(apkPath)
    # time.sleep(15)
    # devices.AdbShellInputTap("关闭启动公告", 636, 701)
    # time.sleep(100)
    # devices.AdbShellInputTap("点击用户协议", 558, 706)
    # time.sleep(2)
    # devices.adbDumpTap("帐号登录", apkPath)
    # time.sleep(2)
    # # devices.adbDumpTap("使用其他方式登录", apkPath)
    # # time.sleep(2)
    # devices.AdbShellInputText("15207676214")
    # time.sleep(2)
    # devices.AdbShellInputTap("点击输入密码", 658, 436)
    # time.sleep(2)
    # devices.AdbShellInputText("123456")
    # time.sleep(2)
    # devices.adbDumpTap("进入游戏", apkPath)
    # time.sleep(5)
    # devices.AdbShellInputTap("关闭公告", 1361, 89)
    # time.sleep(2)
    # devices.AdbShellScreencapPullRm(picture)
    # time.sleep(2)
    # qfvalue = OCRbase(picture, isFix=True, topX=558, bottomX=983, topY=515, bottomY=567)
    # time.sleep(3)
    # data = qfvalue.ocr_QFdata()
    # return is_notice(data)

    # 地下城勇者
    # devices.start_apk(apkPath)
    # time.sleep(15)
    # devices.AdbShellInputTap("关闭启动公告", 636, 701)
    # time.sleep(100)
    # devices.AdbShellInputTap("点击用户协议", 558, 706)
    # time.sleep(2)
    # devices.adbDumpTap("帐号登录", apkPath)
    # time.sleep(2)
    # # devices.adbDumpTap("使用其他方式登录", apkPath)
    # # time.sleep(2)
    # devices.AdbShellInputText("15207676214")
    # time.sleep(2)
    # devices.AdbShellInputTap("点击输入密码", 658, 436)
    # time.sleep(2)
    # devices.AdbShellInputText("123456")
    # time.sleep(2)
    # devices.adbDumpTap("进入游戏", apkPath)
    # time.sleep(5)
    # devices.AdbShellInputTap("关闭公告", 1361, 89)
    # time.sleep(2)
    # devices.AdbShellScreencapPullRm(picture)
    # time.sleep(2)
    # qfvalue = OCRbase(picture, isFix=True, topX=558, bottomX=983, topY=515, bottomY=567)
    # time.sleep(3)
    # data = qfvalue.ocr_QFdata()
    # return is_notice(data)


try:
    data = rule()
    devices.log("开服数据：%s" % data)
    devices.printLog("识别区服", "开服数据：%s" % data)
    value = adb.dataRe(state=0, err="", datas=data)
    if not devices.detaillog:
        print(json.dumps(value), end=" ")
    else:
        pass
    devices.killCurrentGame(apkPath)
except FileNotFoundError as e:
    value = adb.dataRe(state=1, err=str(e), datas="")
    print(json.dumps(value), end=" ")
    devices.killCurrentGame(apkPath)
except TypeError as t:
    value = adb.dataRe(state=1, err=str(t), datas="")
    print(json.dumps(value), end=" ")
    devices.killCurrentGame(apkPath)
except AttributeError as a:
    value = adb.dataRe(state=1, err=str(a), datas="")
    print(json.dumps(value), end=" ")
    devices.killCurrentGame(apkPath)
except IndexError as i:
    value = adb.dataRe(state=1, err=str(i), datas="")
    print(json.dumps(value), end=" ")
    devices.killCurrentGame(apkPath)
except Exception as j:
    value = adb.dataRe(state=1, err=str(j), datas="")
    print(json.dumps(value), end=" ")
    devices.killCurrentGame(apkPath)
