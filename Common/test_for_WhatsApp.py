from appium import webdriver
import appium
import time, unittest

class WhatsApp(unittest.TestCase):
    # Pre-condition of running test case
    def setUp(self) -> None:
        '''Desired capabitity settings'''
        desired_caps = {}
        # Platform, Android or iOS
        desired_caps["platformName"] = "Android"
        # Platform version, Android or iOS version
        desired_caps['platformVersion'] = '7'
        #Check device Name in About setting
        desired_caps['deviceName'] = 'HUAWEI nova'
        # app package name
        # desired_caps['appPackage'] = 'com.whatsapp'
        desired_caps['appPackage'] = 'com.android.deskclock'
        # the first activity from app
        # desired_caps['appActivity'] = 'com.whatsapp.Main'
        desired_caps['appActivity'] = '.AlarmsMainActivity'
        # Reset app status
        desired_caps['noReset'] = True
        #For Android, we us UiAutomation or Espresso
        # desired_caps['automationName'] = 'UiAutomation2'
        # apk file address
        # desired_caps['app'] = r'C:\DevTesters\PycharmProjects\MobileAppsAutomation\APKfile\WhatsApp.apk'

        '''Connect to appium server and initializing automation environment with defined setting'''
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(8)

    def test_Clok(self):
        '''Clock test'''
        pass

if __name__ == '__main__':
    unittest.main()