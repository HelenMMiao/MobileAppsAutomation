from appium import webdriver
import unittest
from Functions.screenshotPhone import screenshotithTimeStamp
import time

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
        desired_caps['appPackage'] = 'com.whatsapp'
        # the first activity from app
        desired_caps['appActivity'] = 'com.whatsapp.Main'
        # Reset app status
        desired_caps['noReset'] = True
        #For Android, we us UiAutomation or Espresso
        desired_caps['automationName'] = 'UiAutomator2'
        # apk file address
        desired_caps['app'] = r'C:\DevTesters\PycharmProjects\MobileAppsAutomation\APKfile\WhatsApp.apk'

        '''Connect to appium server and initializing automation environment with defined setting'''
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(8)

    def test_1_Setup(self):
        '''Open and Setup WhatsApp the first time to use it'''

        # Accept 'Privacy Policy' and 'Terms of Service' at first running.
        agree = self.driver.find_elements_by_id('com.whatsapp:id/eula_accept')
        if agree:
            self.driver.find_element_by_id('com.whatsapp:id/eula_accept').click()

        # Set country and phone number.
        rg = self.driver.find_elements_by_id('com.whatsapp:id/register_phone_toolbar_title')
        if rg:
            country = 'New Zealand'
            self.driver.find_element_by_id('com.whatsapp:id/registration_country').click()
            self.driver.find_element_by_id('com.whatsapp:id/menuitem_search').click()
            self.driver.find_element_by_id('com.whatsapp:id/search_src_text').send_keys(country)
            uiCode = 'new UiSelector().resourceId("android:id/list").childSelector(new UiSelector().text("' + country +'"))'
            self.driver.find_element_by_android_uiautomator(uiCode).click()

            # Verify country code is correct after selecting country.
            countryCode = self.driver.find_element_by_id('com.whatsapp:id/registration_cc')
            self.assertEqual('64', countryCode.text, msg='Country code is wrong for'+country)

            # Input phone number and continue.
            self.driver.find_element_by_id('registration_phone').clear()
            self.driver.find_element_by_id('registration_phone').send_keys('291241517')
            self.driver.find_element_by_id('registration_submit').click()
            self.driver.find_element_by_id('android:id/button1').click()

            # Verify phone number is correct by inputting 6-digit code.
            code6 = input("Please input the 6-digit code")
            self.driver.find_element_by_id('com.whatsapp:id/verify_sms_code_input').send_keys(code6)
            time.sleep(5)

        # WhatsApp permission to backup/restore
        googlePermission = self.driver.find_elements_by_id('com.whatsapp:id/permission_message')
        if googlePermission:
            self.driver.find_element_by_id('com.whatsapp:id/cancel').click()

        # WhatsApp profile setup
        profileInfo = self.driver.find_elements_by_android_uiautomator('new UiSelector().text("Profile info")')
        if profileInfo:
            self.driver.find_element_by_id('com.whatsapp:id/registration_name').clear()
            self.driver.find_element_by_id('com.whatsapp:id/registration_name').send_keys("HelloKitty")
            self.driver.find_element_by_id('com.whatsapp:id/register_name_accept').click()

    def test_2_NewChat(self):
        '''New a chat and giving contact permission if required.'''
        # New a chat.
        self.driver.find_element_by_id('com.whatsapp:id/fab').click()

        # Catch the asking for permission dialog if there is, usually the first time to run
        # Follow step by step to enable contact permission.
        try:
            # Continue on asking for permission dialog.
            self.driver.find_element_by_id('com.whatsapp:id/submit').click()

            # Allow Contacts permission if dialog shows
            contactDialog = self.driver.find_elements_by_id('com.android.packageinstaller:id/permission_message')
            if contactDialog:
                self.driver.find_element_by_id('com.android.packageinstaller:id/do_not_ask_checkbox').click()
                self.driver.find_element_by_id('com.android.packageinstaller:id/permission_allow_button').click()

            # Enable contact permission if app info page shows
            appInfo = self.driver.find_elements_by_android_uiautomator('new UiSelector().text("UNINSTALL")')
            if appInfo:
                self.driver.find_element_by_android_uiautomator('new UiSelector().text("Permissions")').click()
                contactPermission = self.driver.find_element_by_android_uiautomator('new UiSelector().text("Contacts")')
                if not contactPermission:
                    contactPermission.click()
                self.driver.find_element_by_id('android:id/up').click()
                self.driver.press_keycode(4)
        except:
            pass

        # Select the contact to chat
        conversation = "Hello, I am using Whatsapp"
        self.driver.find_element_by_android_uiautomator('new UiSelector().text("Honey")').click()
        inputBox = self.driver.find_element_by_id('entry')
        inputBox.send_keys(conversation)
        self.driver.find_element_by_id('send').click()

        # Verify the conversation is sent successfully.
        conSent = self.driver.find_elements_by_xpath('//*[@resource-id="com.whatsapp:id/message_text"]').pop()
        self.assertEqual(conversation, conSent.text, msg='Message sent out is not right.')


if __name__ == '__main__':
    unittest.main()