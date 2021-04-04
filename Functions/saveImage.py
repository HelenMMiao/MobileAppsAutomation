import time

def saveImagewithTimeStamp(driver):
    timeAppendix = time.strftime('%H%M%S', time.localtime(time.time()))
    picFolder = 'C:\DevTesters\PycharmProjects\MobileAppsAutomation\Pictures'
    screenFile = picFolder + '\image' + timeAppendix + '.png'
    driver.save_screenshot(screenFile)