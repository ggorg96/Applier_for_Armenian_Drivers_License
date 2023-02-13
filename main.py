from selenium import webdriver
import time
from selenium.webdriver.common.by import By

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

if __name__ == '__main__':
    submit()