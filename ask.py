from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def ask(prompt_text):
    # Настраиваем безголовый режим для браузера Firefox
    options = Options()
    options.headless = True

    service = Service('/opt/homebrew/bin/geckodriver')  # Путь к geckodriver
    driver = webdriver.Firefox(service=service, options=options)

    try:
        driver.get("https://www.blackbox.ai/")

        # Явное ожидание появления поля ввода
        prompt_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="chat-input-box"]'))
        )

        prompt_input.send_keys(prompt_text)
        prompt_input.send_keys(Keys.RETURN)  # Нажимаем кнопку "Enter"

        # Явное ожидание появления результата
        result = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '(//p[@class="mb-2 last:mb-0"])[2]'))
        )
        ai_comment = result.text.strip()  # Получаем и очищаем текст

        try:
            # Пробуем преобразовать текст в целое число
            rating = int(ai_comment)
            return rating
        except ValueError:
            print(f"Ошибка преобразования ответа в рейтинг: {ai_comment}")
            return None  # Если не удалось преобразовать в число
    finally:
        driver.quit()
