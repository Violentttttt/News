from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def ai_comment(prompt_text):
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

        time.sleep(10)
        # Явное ожидание появления результата и извлечение текста
        result_div = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH,
                                            '(//div[@class="prose break-words dark:prose-invert prose-p:leading-relaxed prose-pre:p-0 fix-max-with-100"])[2]'))
        )

        ai_comment_result = result_div.text.replace(
            "Summary:", "\n<b>Summary:</b>"
        ).replace(
            "AI Comment:", "\n<b>AI Comment:</b>"
        )
        print(ai_comment_result)
        return ai_comment_result
    finally:
        driver.quit()
