from PyQt6.QtGui import QIntValidator
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from PyQt6.QtWidgets import *
import sys
import threading

url = 'https://roadpolice.am/'

def submit(city_index, public_service_number, phone_number):
    driver = webdriver.Chrome(executable_path='chromedriver/chromedriver_mac_arm64/chromedriver')
    try:
        driver.get(url)
        time.sleep(3)
        driver.find_element(By.XPATH, '/html/body/div/header/div/div[3]/div[2]/div[1]/div/table/tbody/tr/td[1]/button/span/span').click()
        time.sleep(3)
        driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/div/div/div/div[2]/div/form/div[2]/span/span[1]/span/span[2]').click()
        time.sleep(3)
        if city_index == 0:
            driver.find_element(By.XPATH, '/html/body/span/span/span[2]/ul/li/ul/li[2]').click()
        elif city_index == 1:
            driver.find_element(By.XPATH, '/html/body/span/span/span[2]/ul/li/ul/li[3]').click()
        elif city_index == 2:
            driver.find_element(By.XPATH, '/html/body/span/span/span[2]/ul/li/ul/li[4]').click()
        time.sleep(3)
        driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/div/div/div/div[2]/div/form/div[4]/input').send_keys(public_service_number)
        time.sleep(3)
        driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/div/div/div/div[2]/div/form/div[5]/input').send_keys(phone_number)
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
    thread_time_out = 5

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Road Police')
        self.setFixedSize(220, 210)

        self.city_combo_box = QComboBox(self)
        self.city_combo_box.addItems(['Yerevan', 'Gyumri', 'Vanadzor'])
        self.city_combo_box.setFixedSize(210, 30)
        self.city_combo_box.move(5, 10)

        self.public_service_number = QLineEdit(self)
        self.public_service_number.setPlaceholderText('Public Service Number')
        self.public_service_number.setFixedSize(200, 30)
        self.public_service_number.move(10, 50)
        self.public_service_number.setValidator(QIntValidator())
        self.public_service_number.setMaxLength(10)

        self.phone_number = QLineEdit(self)
        self.phone_number.setPlaceholderText('Phone Number')
        self.phone_number.setFixedSize(200, 30)
        self.phone_number.move(10, 90)
        self.phone_number.setValidator(QIntValidator())
        self.phone_number.setMaxLength(8)

        self.time_out_combo_box = QComboBox(self)
        self.time_out_combo_box.addItems(['Resubmit in each 5 minutes', 'Resubmit in each 10 minutes', 'Resubmit in each 15 minutes'])
        self.time_out_combo_box.setFixedSize(210, 30)
        self.time_out_combo_box.move(5, 130)
        self.time_out_combo_box.currentIndexChanged.connect(self.thread_time_out_change)

        self.start_button = QPushButton(self)
        self.start_button.setText('Start')
        self.start_button.setFixedSize(95, 30)
        self.start_button.move(10, 170)
        self.start_button.clicked.connect(self.start_button_handler)

        self.stop_button = QPushButton(self)
        self.stop_button.setText('Stop')
        self.stop_button.setFixedSize(95, 30)
        self.stop_button.move(115, 170)
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
            submit(self.city_combo_box.currentIndex(), self.public_service_number.text(), self.phone_number.text())
            for i in range(0, self.thread_time_out*60, 3):
                time.sleep(3)
                if self.stop_thread:
                    break

    def thread_time_out_change(self):
        if self.time_out_combo_box.currentIndex() == 0:
            self.thread_time_out = 5
        elif self.time_out_combo_box.currentIndex() == 1:
            self.thread_time_out = 10
        elif self.time_out_combo_box.currentIndex() == 2:
            self.thread_time_out = 15

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()