import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = int(timeout)
        self.wait = WebDriverWait(driver, timeout)
        self.page_url = ''

    def find_element(self, by: By or int, value: str) -> WebElement:
        return self.wait.until(expected_conditions.visibility_of_element_located((by, value)),
                               message=f'Элемент {by, value} не найден')

    def find_elements(self, by: By or int, value: str) -> [WebElement]:
        return self.wait.until(expected_conditions.visibility_of_all_elements_located((by, value)),
                               message=f'Элементы {by, value} не найдены')

    def get_current_url(self) -> str:
        return self.driver.current_url


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, timeout=60)

        self.login = (By.ID, 'user-name')  # Локатор по ID для элемента строки ввода login
        self.password = (By.ID, 'password')  # Локатор по ID для элемента строки ввода password
        self.login_btn = (By.NAME, 'login-button')  # Локатор по Name для элемента кнопка Login

    def auth(self, login: str, password: str) -> None:
        self.find_element(*self.login).send_keys(login)
        self.find_element(*self.password).send_keys(password)
        self.find_element(*self.login_btn).click()

    @allure.step(r'Ввести логин')
    def input_login(self, login: str) -> None:
        self.find_element(*self.login).send_keys(login)

    @allure.step(r'Ввести пароль"')
    def input_password(self, password: str) -> None:
        self.find_element(*self.password).send_keys(password)

    @allure.step(r'Нажать кнопку "LOGIN"')
    def login_button_click(self) -> None:
        self.find_element(*self.login_btn).click()


class InventoryPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, timeout=60)

        self.page_url = 'https://www.saucedemo.com/inventory.html'
        # Заголовок любого товара: Здесь будет локатор по ID
        self.item = (By.ID, 'item_4_title_link')
        # Кнопка Add to Cart для Sauce Labs Fleece Jacket: Здесь будет локатор XPATH
        self.add_jacket_to_cart_btn = (By.XPATH, '//*[@id="add-to-cart-sauce-labs-fleece-jacket"]')
        # Кнопка корзины: Здесь будет локатор XPATH
        self.cart_btn = (By.XPATH, '//*[@class="shopping_cart_link"]')

    def choose_item(self):
        self.find_element(*self.item).click()

    def add_jacket_to_cart_btn_click(self):
        self.find_element(*self.add_jacket_to_cart_btn).click()

    def cart_btn_click(self):
        self.find_element(*self.cart_btn).click()

    @allure.step(r'Проверить, что открыта страница "https://www.saucedemo.com/inventory.html"')
    def check_inventory_page_open(self) -> None:
        assert self.get_current_url() == self.page_url, (
            '[Failed] Login attempt was failed, check login and password'
        )


class ItemPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, timeout=60)

        # Кнопка Add to Cart: Здесь будет локатор XPATH
        self.add_to_cart_btn = (By.XPATH, '//*[@name="add-to-cart"]')
        # Кнопка Back to products: Здесь будет локатор XPATH
        self.back_to_products = (By.XPATH, '//*[@name="back-to-products"]')

    def add_to_cart_btn_click(self):
        self.find_element(*self.add_to_cart_btn).click()

    def return_to_products(self):
        self.find_element(*self.back_to_products).click()


class CartPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, timeout=60)

        # Локатор XPATH элемента продукта. Локатор должен
        # находить ровно 2 элемента на странице: первый и второй товар,
        # то есть в DevTools вы должны видеть "1 of 2" при поиске данного локатора
        self.item_list = (By.XPATH, '//*[@class="cart_item"]')

    def number_of_products(self):
        return len(self.find_elements(*self.item_list))
