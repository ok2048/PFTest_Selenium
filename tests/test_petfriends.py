from conftest import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_show_all_pets(driver, login):
    '''Проверка наличия фото, клички, вознаста и породы у всех питомцев на главной странице'''
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    # Задаем таймаут для неявного ожидания
    driver.implicitly_wait(5)
    # Проверяем, что у каждого питомца есть изображение, кличка, возраст и вид
    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''  # изображение
        assert names[i].text != ''  # кличка
        assert descriptions[i].text != ''
        # Вид и возраст содержатся в поле descriptions через запятую
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0  # вид
        assert len(parts[1]) > 0  # возраст


def test_all_my_pets_are_shown(driver, login):
    '''Проверка, что все питомцы пользователя отображаются на странице "Мои питомцы"'''
    # Переходим на страницу "Мои питомцы"
    driver.find_element(By.XPATH, '//a[@href="/my_pets"]').click()
    wait = WebDriverWait(driver, 5)
    user_elem = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class=".col-sm-4 left"]')))
    # Из информации о пользователе выделяем количество его питомцев
    str_n_of_all_pets = user_elem.text.split('\n')[1]
    n_of_all_pets = int(str_n_of_all_pets.split(':')[1])

    # Проверяем, что количество выведенных питомцев совпадает со статистикой пользователя
    # (количество строк в таблице минус заголовок)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tr')))
    list_of_shown_anmls = driver.find_elements(By.CSS_SELECTOR, 'tr')
    assert n_of_all_pets == len(list_of_shown_anmls) - 1


def test_half_my_pets_have_photo(driver, login):
    '''Проверка, что хотя бы у половины питомцев пользователя есть фото'''
    # Переходим на страницу "Мои питомцы"
    driver.find_element(By.XPATH, '//a[@href="/my_pets"]').click()
    wait = WebDriverWait(driver, 5)
    user_elem = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class=".col-sm-4 left"]')))
    # Из информации о пользователе выделяем количество его питомцев
    str_n_of_all_pets = user_elem.text.split('\n')[1]
    n_of_all_pets = int(str_n_of_all_pets.split(':')[1])
    # Инициализируем счетчик изображений
    n_of_imgs = 0

    # Проверяем количество фото
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'th>img')))
    images = driver.find_elements(By.CSS_SELECTOR, 'th>img')

    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            n_of_imgs += 1

    # Фото хотя бы у половины
    assert n_of_imgs >= (n_of_all_pets // 2 + n_of_all_pets % 2)


def test_all_my_pets_have_name_age_type(driver, login):
    '''Проверка, что у всех питомцев пользователя есть кличка, возраст и порода'''
    # Переходим на страницу "Мои питомцы"
    driver.find_element(By.XPATH, '//a[@href="/my_pets"]').click()
    wait = WebDriverWait(driver, 5)
    user_elem = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class=".col-sm-4 left"]')))
    # Из информации о пользователе выделяем количество его питомцев
    str_n_of_all_pets = user_elem.text.split('\n')[1]
    n_of_all_pets = int(str_n_of_all_pets.split(':')[1])
    # Инициализируем счетчики кличек, возрастов и пород на странице
    n_of_names = 0
    n_of_ages = 0
    n_of_anmltypes = 0

    # Проверяем количество кличек, возрастов и пород
    wait.until(EC.presence_of_element_located((By.XPATH, '//tr/td[1]')))
    names = driver.find_elements(By.XPATH, '//tr/td[1]')  # клички
    wait.until(EC.presence_of_element_located((By.XPATH, '//tr/td[2]')))
    anmltypes = driver.find_elements(By.XPATH, '//tr/td[2]')  # породы
    wait.until(EC.presence_of_element_located((By.XPATH, '//tr/td[3]')))
    ages = driver.find_elements(By.XPATH, '//tr/td[3]')  # возрасты

    for i in range(len(names)):
        if names[i].text != '':
            n_of_names += 1
        if anmltypes[i].text != '':
            n_of_anmltypes += 1
        if ages[i].text != '':
            n_of_ages += 1

    # Кличка, порода, возраст у всех
    assert n_of_names == n_of_all_pets
    assert n_of_ages == n_of_all_pets
    assert n_of_anmltypes == n_of_all_pets


def test_all_my_pets_have_unique_names(driver, login):
    '''Проверка, что все питомцы пользователя имеют уникальные клички'''
    # Переходим на страницу "Мои питомцы"
    driver.find_element(By.XPATH, '//a[@href="/my_pets"]').click()
    wait = WebDriverWait(driver, 5)
    user_elem = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class=".col-sm-4 left"]')))
    # Из информации о пользователе выделяем количество его питомцев
    str_n_of_all_pets = user_elem.text.split('\n')[1]
    n_of_all_pets = int(str_n_of_all_pets.split(':')[1])

    # Инициализируем множество уникальных кличек
    unique_names = set()

    # Заполняем множество кличек и проверяем,
    # что количество элементов в нем совпадает с количеством питомцев
    wait.until(EC.presence_of_element_located((By.XPATH, '//tr/td[1]')))
    names = driver.find_elements(By.XPATH, '//tr/td[1]')  # клички

    for i in range(len(names)):
        unique_names.add(names[i].text)

    # Все клички уникальные
    assert len(unique_names) == n_of_all_pets


def test_all_my_pets_are_unique(driver, login):
    '''Проверка, что все питомцы пользователя уникальны.
    Повторяющиеся питомцы — это питомцы, у которых одинаковые кличка, порода и возраст.'''
    # Переходим на страницу "Мои питомцы"
    driver.find_element(By.XPATH, '//a[@href="/my_pets"]').click()
    wait = WebDriverWait(driver, 5)
    user_elem = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class=".col-sm-4 left"]')))
    # Из информации о пользователе выделяем количество его питомцев
    str_n_of_all_pets = user_elem.text.split('\n')[1]
    n_of_all_pets = int(str_n_of_all_pets.split(':')[1])
    # Инициализируем множество уникальных питомцев
    unique_pets = set()

    # Заполняем множество питомцев и проверяем,
    # что количество элементов в нем совпадает с количеством питомцев
    wait.until(EC.presence_of_element_located((By.XPATH, '//tr/td[1]')))
    names = driver.find_elements(By.XPATH, '//tr/td[1]')  # клички
    wait.until(EC.presence_of_element_located((By.XPATH, '//tr/td[2]')))
    anmltypes = driver.find_elements(By.XPATH, '//tr/td[2]')  # породы
    wait.until(EC.presence_of_element_located((By.XPATH, '//tr/td[3]')))
    ages = driver.find_elements(By.XPATH, '//tr/td[3]')  # возрасты

    for i in range(len(names)):
        # Добавляем текущего питомца в множество питомцев
        curr_pet = (names[i].text, anmltypes[i].text, ages[i].text)
        unique_pets.add(curr_pet)

    # Все питомцы уникальные
    assert len(unique_pets) == n_of_all_pets
