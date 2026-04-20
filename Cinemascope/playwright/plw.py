# plw.py
import time
from playwright.sync_api import Page
from Cinemascope.playwright.conf import my_page  # Импортируем my_page


def test_text_box(my_page: Page):
    print("\n=== ТЕСТ В plw.py ===")
    print("Переходим на сайт...")
    my_page.goto('https://demoqa.com/text-box')
    print(f"Страница открыта: {my_page.url}")

    print("Заполняем поле...")
    my_page.fill(selector='#userName', value='testQa')
    print("Поле заполнено")

    print("Браузер открыт, ждем 10 секунд...")
    time.sleep(10)
    print("=== ТЕСТ ЗАВЕРШЕН ===")