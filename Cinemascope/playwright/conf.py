import pytest
from playwright.sync_api import sync_playwright, Page, expect, Playwright
import time
from random import randint
from pathlib import Path

from datetime import datetime
from playwright.sync_api import expect


class Tools:
    @staticmethod
    def project_dir():
        """
        Возвращает корневую директорию проекта.
        Предполагается, что текущий файл находится в поддиректории `common`.
        """
        return Path(__file__).parent.parent

    @staticmethod
    def files_dir(nested_directory: str = None, filename: str = None):
        """
        Возвращает путь к директории `files` (или её поддиректории).
        Если директория не существует, она создается.
        Если указан `filename`, возвращает полный путь к файлу.
        """
        files_path = Tools.project_dir() / "files"
        if nested_directory:
            files_path = files_path / nested_directory
        files_path.mkdir(parents=True, exist_ok=True)

        if filename:
            return files_path / filename
        return files_path

    @staticmethod
    def get_timestamp():
        """
        Возвращает текущую временную метку в формате YYYY-MM-DD_HH-MM-SS.
        """
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

DEFAULT_UI_TIMEOUT = 30000  # Пример значения таймаута


@pytest.fixture(scope="session")  # Браузер запускается один раз для всей сессии
def browser(playwright):
    browser = playwright.chromium.launch(headless=False)  # headless=True для CI/CD, headless=False для локальной разработки
    yield browser  # yield возвращает значение фикстуры, выполнение теста продолжится после yield
    browser.close()  # Браузер закрывается после завершения всех тестов


@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    context.set_default_timeout(DEFAULT_UI_TIMEOUT)
    yield context
    log_name = f"trace_{Tools.get_timestamp()}.zip"
    trace_path = Tools.files_dir('playwright_trace', log_name)
    context.tracing.stop(path=trace_path)
    context.close()

@pytest.fixture(scope="function")  # Страница создается для каждого теста
def page(context):
    page = context.new_page()
    yield page  # yield возвращает значение фикстуры, выполнение теста продолжится после yield
    page.close()  # Страница закрывается после завершения теста


# def test_text_box(page: Page):
#     page.goto('https://demoqa.com/text-box')
#
#     username_locator = '#userName'
#     page.fill(username_locator, 'testQa')
#     page.fill('#userEmail', 'test@qa.com')
#     page.fill('#currentAddress', 'Phuket, Thalang 99')
#     page.fill('#permanentAddress', 'Moscow, Mashkova 1')
#
#     page.click('button#submit')
#
#     expect(page.locator('#output #name')).to_have_text('Name:testQa')
#     expect(page.locator('#output #email')).to_have_text('Email:test@qa.com')
#     expect(page.locator('#output #currentAddress')).to_have_text('Current Address :Phuket, Thalang 99')
#     expect(page.locator('#output #permanentAddress')).to_have_text('Permananet Address :Moscow, Mashkova 1')


#



#

# def test_registration(page: Page):
#     page.pause()
#     page.goto('https://dev-cinescope.coconutqa.ru/register')
#
#     user_password = 'Qwerty12345'
#     user_email = f'test{randint(1, 9999)}@coconutqa.ru'
#
#     # Заполняем форму
#     page.fill('input[name="fullName"]', 'Валерий Жмышенко')
#     page.fill('input[name="email"]', user_email)
#     page.fill('input[name="password"]', user_password)
#     page.fill('input[name="passwordRepeat"]', user_password)
#
#     # Нажимаем кнопку и ждем перехода
#     page.click('button[type="submit"]')
#
#     # Ждем перехода на страницу подтверждения
#     page.wait_for_url('https://dev-cinescope.coconutqa.ru/login')
#     expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(visible=True)
#
#     time.sleep(15)

#
# def test_demqa(page: Page):
#
#     page.goto('https://demoqa.com/webtables')
#
#     page.locator('button', has_text="Add").click()
#
#     is_visible = page.get_by_text('Registration Form').is_visible()
#     print(is_visible)
#     page.get_by_placeholder("First Name").fill("Oleg")
#     page.get_by_placeholder("Last Name").fill("Filippov")
#     page.get_by_placeholder("name@example.com").fill("Filippov@1.ru")
#     page.get_by_placeholder("Age").fill("32")
#     page.get_by_placeholder("Salary").fill("100")
#     page.get_by_placeholder("Department").fill("QA")
#
#     page.click('button[type="submit"]')
#     time.sleep(15)
#

# def test_demqa(page: Page):
#
#     page.goto('https://demoqa.com/automation-practice-form')
#
#     # page.locator('button', has_text="Add").click()
#
#     page.get_by_role('textbox', name='First Name').fill("Oleg")
#     page.get_by_role('textbox', name='Last Name').fill("Filippov")
#     page.get_by_role('textbox', name='name@example.com').fill("Filippov@mail.ru")
#     page.get_by_role('radio', name='Male', exact=True).check()
#     page.get_by_role('textbox', name='Mobile Number').fill("89831552296")
#     page.locator('#subjectsContainer div').nth(3).click()
#     page.keyboard.type('Biology')
#     page.get_by_role('option', name='Biology').click()
#     page.get_by_role('checkbox', name='Sports').check()
#     page.get_by_role('textbox', name='Current Address').fill("Moscow, Mira 7G")
#     page.locator('#state').click()
#     page.get_by_text('NCR', exact=True).click()
#     page.locator('#city').click()
#     page.get_by_text('Delhi', exact=True).click()
#
#     today_date = datetime.now().strftime("%d %b %Y")
#     expect(page.locator('#dateOfBirthInput')).to_have_value(today_date)
#     expect(page.get_by_text('© 2013-2026 TOOLSQA.COM | ALL RIGHTS RESERVED.')).to_contain_text('© 2013-2026 TOOLSQA.COM | ALL')
#
#
#
#     page.click('button[type="submit"]')
#
#     page.get_by_role('button', name='Close').click()
#     time.sleep(15)
#
#
# def test_demqa1(page: Page):
#
#     page.goto('https://demoqa.com/radio-button')
#
#     expect(page.locator('#yesRadio')).to_be_enabled()
#     expect(page.locator('#impressiveRadio')).to_be_enabled()
#     expect(page.locator('#noRadio')).to_be_disabled()
#
#
#
# def test_demqa2(page: Page):
#
#     page.goto('https://demoqa.com/checkbox')
#
#
#     expect(page.get_by_text('Home')).to_be_visible()
#     expect(page.get_by_text('Desktop')).not_to_be_visible()
#     page.locator('.rc-tree-switcher.rc-tree-switcher_close').click()
#     expect(page.get_by_text('Desktop')).to_be_visible()
#
# def test_demqa3(page: Page):
#
#     page.goto('https://demoqa.com/dynamic-properties')
#
#     expect(page.locator("#visibleAfter")).not_to_be_visible()
#     page.wait_for_selector("#visibleAfter")
#     expect(page.locator("#visibleAfter")).to_be_visible()

#Modul_4\PlaywrightExamples\page_object_models.py
import time
from playwright.sync_api import sync_playwright

# Перед запуском выполните
# pip install playwright
# python -m playwright install
#=============================================================================================================================================================
# Простой пример (пункт "Как это работает?")

class GooglePage:
    def __init__(self, page):
        self.page = page
        self.url = "https://www.google.com/"

        # Локаторы элементов
        self.search_input = 'textarea[name="q"]'  # Поле ввода запроса
        self.search_button = 'input[value="Поиск в Google"]'  # Кнопка "Поиск Google"
        self.lucky_button = 'input[value="Мне повезёт"]'  # Кнопка "Мне повезёт"

    def open(self):
        """Открывает страницу Google."""
        self.page.goto(self.url)

    def enter_search_query(self, query):
        """Вводит текст в строку поиска."""
        self.page.fill(self.search_input, query)

    def click_search_button(self):
        """Нажимает кнопку 'Поиск Google'."""
        self.page.click(self.search_button)

    def click_lucky_button(self):
        """Нажимает кнопку 'Мне повезёт'."""
        self.page.click(self.lucky_button)


def test_page_objec():
   with sync_playwright() as playwright:
        # Запуск браузера
        browser = playwright.chromium.launch(headless=False)  # headless=False для визуального отображения
        page = browser.new_page()

        # Создаем объект страницы Google
        google_page = GooglePage(page)

        # Открываем Google
        google_page.open()

        # Вводим запрос и нажимаем кнопку "Поиск Google"
        google_page.enter_search_query("Аниме")
        # time.sleep(2)
        google_page.enter_search_query("Вакансии ?")
        # time.sleep(2)
        google_page.enter_search_query("Page Object что это?")
        # time.sleep(3)
        google_page.click_search_button()
        time.sleep(10)

        # Ждем завершения поиска (например, появления заголовка страницы)
        page.wait_for_selector("h3")  #раскоментируйте если хотите чтоб браузер не закрывался

        # Закрываем браузер
        browser.close()



