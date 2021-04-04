from appium import webdriver
import unittest
from Functions.screenshotPhone import screenshotithTimeStamp
import time

# Time alarm to be set and deleted
alarmSet = ['10:40', 'am']

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

    # def test_x(self):
    #     alarmH = alarmSet[0].split(':')[0]
    #     print(alarmH)

    def test_1_setClock(self):
        '''Set an new alarm, repeat every Monday, customerized Rington and label'''

        alarmH = alarmSet[0].split(':')[0]
        alarmM = alarmSet[0].split(':')[1]
        alarmX = alarmSet[1].upper()

        # Get the alarm list before creating alarm, which will be compared later to get the new alarm
        alarmListOld = self.driver.find_elements_by_id('alarms_list')

        # Open Add alarm page and get alarm setting data.
        self.driver.find_element_by_id('alarm_new_btn').click()
        alarmTime = self.driver.find_elements_by_xpath(
            "//*[@resource-id='android:id/timePickerLayout']//*[@resource-id='android:id/numberpicker_input']")

        '''Set the alarm time as expected'''
        # Set alarm hour as specified
        while (alarmTime[0].text != alarmH):
            self.driver.swipe(270, 671, 270, 549, 1000)
        # Set alarm minutes as specified
        while (alarmTime[1].text != alarmM):
            self.driver.swipe(540, 671, 540, 549, 1000)
        # Set to AM alarm.
        if (alarmTime[2].text != alarmX):
            self.driver.swipe(810, 427, 810, 549, 1000)

        # Set alarm to repeat every Monday, by using UiAutomator code.
        self.driver.find_element_by_id('textarrow_repeat_layout').click()
        # self.driver.find_element_by_xpath("//*[@resource-id = 'android:id/select_dialog_listview']/*[last()]").click()
        # self.driver.find_element_by_xpath("//*[@resource-id='android:id/select_dialog_listview']/*[2]").click()

        # Locate the element using uiautomator.
        self.driver.find_element_by_android_uiautomator('new UiSelector().text("Custom")').click()
        self.driver.find_element_by_android_uiautomator('new UiSelector().text("Monday")').click()
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
        lableInput.clear()
        lableInput.send_keys('Appium Test')
        self.driver.find_element_by_id('android:id/button1').click()

        # Save the alarm set.
        self.driver.find_element_by_accessibility_id('Done').click()

        # Screenshot of the screen and pull to computer.
        screenshotithTimeStamp()

        # Check the alarm list and make sure the alarm is added successfully.
        alarmListNew = self.driver.find_elements_by_id('alarms_list')
        for alarm in alarmListNew:
            print(alarm.text)
            if alarm in alarmListOld:

                print('Old one')
            else:
                print('new one')
                self.assertEqual(alarmSet[0], alarm.find_element_by_xpath(".//*[@resource-id='com.android.deskclock:id/digital_full_time']").text, msg='Alarm Time is not correct')
                self.assertEqual(alarmSet[1].upper(), alarm.find_element_by_xpath(".//*[@resource-id='com.android.deskclock:id/digital_right_ampm']").text.strip(), msg='Alarm AMPM is not correct')
                self.assertEqual('Appium Test, Mon', alarm.find_element_by_xpath(".//*[@resource-id='com.android.deskclock:id/daysOfWeek']").text, msg='Repeat is not correct')


    def test_2_deleteClock(self):
        # Find the new set alarm and delete it.
        alarmList = self.driver.find_elements_by_xpath('//*[@resource-id="com.android.deskclock:id/digitalClock"]')
        alarmNumberOld = len(alarmList)
        # print(alarmNumberOld)
        for alarm in alarmList:

            if (alarm.find_element_by_xpath('.//*[@resource-id="com.android.deskclock:id/digital_full_time"]').text == alarmSet[0] and
                alarm.find_element_by_xpath('.//*[@resource-id="com.android.deskclock:id/digital_right_ampm"]').text.strip() ==alarmSet[1].upper()):
                alarm.find_element_by_class_name('android.widget.LinearLayout').click()
                self.driver.find_element_by_id('delete_alarm').click()
                self.driver.find_element_by_id('android:id/button1').click()
                time.sleep(2)


        # Check that the new added alarm is deleted.
        alarmNumberNew = len(self.driver.find_elements_by_xpath('//*[@resource-id="com.android.deskclock:id/digitalClock"]'))
        self.assertLess(alarmNumberNew, alarmNumberOld,msg="Alarm not deleted successfully")

        # Screenshot after deleting alarm.
        screenshotithTimeStamp()



if __name__ == '__main__':
    unittest.main()