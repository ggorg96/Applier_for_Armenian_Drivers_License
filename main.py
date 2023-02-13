from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from PyQt6.QtWidgets import *
import sys
import threading

url = 'https://roadpolice.am/'

def submit():
    driver = webdriver.Chrome(executable_path='chromedriver/chromedriver_mac_arm64/chromedriver')
    try:
        driver.get(url)
        time.sleep(3)
        driver.find_element(By.XPATH, '/html/body/div/header/div/div[3]/div[2]/div[1]/div/table/tbody/tr/td[1]/button/span/span').click()
        time.sleep(3)
        driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/div/div/div/div[2]/div/form/div[2]/span/span[1]/span/span[2]').click()
        time.sleep(3)
        driver.find_element(By.XPATH, '/html/body/span/span/span[2]/ul/li/ul/li[2]').click()
        time.sleep(3)
        driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/div/div/div/div[2]/div/form/div[4]/input').send_keys('1234567890')
        time.sleep(3)
        driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/div/div/div/div[2]/div/form/div[5]/input').send_keys('12345678')
        time.sleep(3)
        driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/div/div/div/div[2]/div/form/div[6]/button').click()
        time.sleep(3)
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()

class MainWindow(QMainWindow):
    thread = None
    stop_thread = False

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Road Police')
        self.setFixedSize(220, 50)

        self.start_button = QPushButton(self)
        self.start_button.setText('Start')
        self.start_button.setFixedSize(95, 30)
        self.start_button.move(10, 10)
        self.start_button.clicked.connect(self.start_button_handler)

        self.stop_button = QPushButton(self)
        self.stop_button.setText('Stop')
        self.stop_button.setFixedSize(95, 30)
        self.stop_button.move(115, 10)
        self.stop_button.clicked.connect(self.stop_button_handler)
        self.stop_button.setDisabled(True)

    def start_button_handler(self):
        self.start_button.setDisabled(True)
        self.stop_button.setEnabled(True)

        self.stop_thread = False
        self.thread = threading.Thread(target=self.submitting_thread)
        self.thread.start()

    def stop_button_handler(self):
        self.start_button.setEnabled(True)
        self.stop_button.setDisabled(True)

        self.stop_thread = True
        self.thread.join()

    def submitting_thread(self):
        while not self.stop_thread:
            submit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()