import os
import time

def screenshotithTimeStamp():
    timeAppendix = time.strftime('%H%M%S', time.localtime(time.time()))
    adbScreenShot = 'adb shell screencap /sdcard/screen'+timeAppendix+'.png'
    os.system(adbScreenShot)
    adbPullScreen = 'adb pull /sdcard/screen'+timeAppendix+'.png C:/DevTesters/PycharmProjects/MobileAppsAutomation/Pictures/'
    os.system(adbPullScreen)

    # os.system('adb shell screencap /sdcard/screen3.png && adb pull /sdcard/screen3.png')
