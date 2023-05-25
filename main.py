from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import time
import random
import sys

data = {}

linkZ = sys.argv[1]

for _ in range(1):  # Запустить весь процесс 2 раза
    # Настройка опций для Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    # Инициализация драйвера
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(linkZ)

    prev_links_count = 0

    for _ in range(1):  # Будет выполнено два раза
        # Найдем все элементы 'a' с заданными классами и атрибутом itemprop="url"
        link_elements = driver.find_elements(By.CSS_SELECTOR, 'a.styles-module-root-QmppR.styles-module-root_noVisited-aFA10[itemprop="url"]')

        # Сохраняем все ссылки в список
        links = [link.get_attribute('href') for link in link_elements if link.get_attribute('href') not in data]  # Проверка на дублирование данных

        if len(links) == prev_links_count:
            break  # Если число ссылок не изменилось, прерываем цикл

        prev_links_count = len(links)  # Обновляем число ссылок для следующей итерации

        # Переберем все ссылки и посещаем каждую
        for link in links:
            driver.get(link)

            # Случайная задержка от 1 до 50 секунд
            time.sleep(random.randint(1, 1))

            # Поиск div элемента с заданным XPath
            try:
                div_element = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[1]/div/div[2]/div[3]/div[1]/div[2]/div[1]/div[3]/div')

                # Найти все элементы li в этом div
                li_elements = div_element.find_elements(By.CSS_SELECTOR, 'ul li')

                # Сохранение содержимого списка li в данные
                data[link] = [li.text for li in li_elements]
            except:
                print(f"Не удалось найти div для {linkZ}.")

            # Возвращаемся на исходную страницу
            driver.get(linkZ)

        # Прокрутка страницы до конца
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        print('Скролл вниз!')
        time.sleep(5)  # Подождите, пока появятся новые ссылки

    driver.quit()

# Сохранение JSON
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)
