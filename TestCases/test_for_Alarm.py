from appium import webdriver
import unittest
import time



class AlarmTest(unittest.TestCase):
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
        desired_caps['appPackage'] = 'com.android.deskclock'
        # the first activity from app
        desired_caps['appActivity'] = '.AlarmsMainActivity'
        # Reset app status
        desired_caps['noReset'] = True
        #For Android, we us UiAutomation or Espresso
        desired_caps['automationName'] = 'UiAutomator2'
        # apk file address
        # desired_caps['app'] = r'C:\DevTesters\PycharmProjects\MobileAppsAutomation\APKfile\WhatsApp.apk'

        '''Connect to appium server and initializing automation environment with defined setting'''
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(8)

    def test_setClock(self):
        '''
         Set an new alarm at 9:00 am,
         repeat every Monday, customerized Rington and label
         '''
        # The alarm time user wants to set
        alarmSet = ['2:30', 'am']
        alarmH = alarmSet[0].split(':')[0]
        alarmM = alarmSet[0].split(':')[1]
        alarmX = alarmSet[1].upper()

        #Open Add alarm page and get alarm setting data.
        self.driver.find_element_by_id('alarm_new_btn').click()
        alarmTime = self.driver.find_elements_by_xpath("//*[@resource-id='android:id/timePickerLayout']//*[@resource-id='android:id/numberpicker_input']")

        #Set the alarm hour as specified
        while (alarmTime[0].text != alarmH):
            self.driver.swipe(270, 671, 270, 549, 1000)

        #Set alarm minutes as specified
        while (alarmTime[1].text != alarmM):
            self.driver.swipe(540, 671, 540, 549, 1000)

        #Set to AM alarm.
        if (alarmTime[2].text != alarmX):
            self.driver.swipe(810, 427, 810, 549, 1000)

        # Set alarm to repeat every Monday
        self.driver.find_element_by_id('textarrow_repeat_layout').click()
        self.driver.find_element_by_xpath("//*[@resource-id = 'android:id/select_dialog_listview']/*[last()]").click()
        self.driver.find_element_by_xpath("//*[@resource-id='android:id/select_dialog_listview']/*[2]").click()
        # self.driver.find_element_by_xpath("//*[@resource-id='android:id/button1']").click()
        self.driver.find_element_by_id("android:id/button1").click()

        # Set Ringtone to the fouth listed.
        self.driver.find_element_by_id('textarrow_ringtone_layout').click()
        self.driver.find_element_by_xpath("//*[@resource-id = 'com.huawei.android.thememanager:id/lv_local_ringtone']/*[4]").click()
        self.driver.find_element_by_id('android:id/icon2').click()

        #Make sure Vibrate is set to OFF
        alarmVibrate = self.driver.find_element_by_id('switch_vibrate_layout')
        # print(alarmVibrate.find_element_by_id("android:id/switch_widget").get_attribute('checked'))
        if alarmVibrate.find_element_by_id("android:id/switch_widget").get_attribute('checked'):
            alarmVibrate.click()
        #
        # Input customerized alarm label
        self.driver.find_element_by_id('textarrow_label_layout').click()
        lableInput = self.driver.find_element_by_id("username_edit")
        #Clear the label input before inputing customer one.
        lableInput.clear()
        lableInput.send_keys('Appium Test')
        self.driver.find_element_by_id('android:id/button1').click()
        #
        # #Save the alarm set.
        self.driver.find_element_by_id('android:id/icon2').click()


if __name__ == '__main__':
    unittest.main()