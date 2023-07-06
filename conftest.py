import pytest as pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture(scope='session', autouse=True)
def driver():
   driver = webdriver.Chrome()
   # Переходим на страницу авторизации
   driver.get('https://petfriends.skillfactory.ru/login')

   yield driver

   driver.quit()

@pytest.fixture(scope='session', autouse=True)
def login(driver):
   # Вводим email
   driver.find_element(By.ID, 'email').send_keys('qappp@qap1028.qap')
   # Вводим пароль
   driver.find_element(By.ID, 'pass').send_keys('12345')
   # Нажимаем на кнопку входа в аккаунт
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()