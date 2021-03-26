import unittest
from selenium import webdriver
import saveImage


class TempFile(unittest.TestCase):
    def setUp(self) -> None:
        pass
    def tearDown(self) -> None:
        pass

    def test_1(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.google.com/')
        saveImage.saveImagewithTimeStamp(self.driver)

if __name__ == '__main__':
    unittest.main()

